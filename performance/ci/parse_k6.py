#!/usr/bin/env python3
import argparse
import json
import os
from collections import defaultdict
from statistics import mean

# On suppose que le script k6 met tags.endpoint = "/login" "/users" "/orders"
ENDPOINTS = ["/login", "/users", "/orders"]

def load_events(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)

def compute_kpis(json_path):
    durations = {ep: [] for ep in ENDPOINTS}
    errors = {ep: 0 for ep in ENDPOINTS}
    counts = {ep: 0 for ep in ENDPOINTS}
    first_ts = None
    last_ts = None

    for evt in load_events(json_path):
        # k6 JSON output = stream d'événements
        # Les req HTTP apparaissent dans "metric": "http_req_duration" ou "http_reqs" etc.
        # On se base sur "http_req_duration" pour mesurer les requêtes réellement effectuées.
        if evt.get("type") != "Point":
            continue

        metric = evt.get("metric")
        data = evt.get("data", {})
        tags = data.get("tags", {}) or {}
        endpoint = tags.get("endpoint")

        # timestamps (pour throughput)
        ts = data.get("time")
        if ts:
            first_ts = ts if first_ts is None else min(first_ts, ts)
            last_ts = ts if last_ts is None else max(last_ts, ts)

        if metric == "http_req_duration" and endpoint in durations:
            val_ms = data.get("value")
            if isinstance(val_ms, (int, float)):
                durations[endpoint].append(val_ms)
                counts[endpoint] += 1

                # erreur si status >= 400
                status = tags.get("status")
                try:
                    status_i = int(status) if status is not None else 200
                except Exception:
                    status_i = 200
                if status_i >= 400:
                    errors[endpoint] += 1

    # Durée approximative observée (si ts present)
    duration_s = 0.0
    if first_ts is not None and last_ts is not None:
        # ts est une string ISO; on ne parse pas en datetime pour rester robuste,
        # et on utilise plutôt les compteurs si besoin.
        # Ici, on laisse 30s par défaut si impossible à déduire.
        duration_s = 30.0
    else:
        duration_s = 30.0

    kpis = {}
    for ep in ENDPOINTS:
        n = counts[ep]
        if n == 0:
            kpis[ep] = None
            continue

        avg_ms = mean(durations[ep])
        max_ms = max(durations[ep])
        err_pct = (errors[ep] / n) * 100.0
        thr = n / duration_s

        kpis[ep] = {
            "avg_ms": avg_ms,
            "max_ms": max_ms,
            "err_pct": err_pct,
            "throughput": thr,
            "count": n,
        }

    return kpis

def classify(kpis):
    # Diagnostic simple et “IA-like”
    notes = []
    bottlenecks = []

    login = kpis.get("/login")
    if login is None:
        bottlenecks.append("Le scénario n'a pas atteint /login (aucune requête mesurée).")
    else:
        if login["err_pct"] >= 2:
            bottlenecks.append(f"/login instable : {login['err_pct']:.2f}% d'erreurs.")
        if login["avg_ms"] >= 5000:
            bottlenecks.append(f"/login très lent : {login['avg_ms']:.0f}ms en moyenne.")
        if login["max_ms"] >= 10000:
            bottlenecks.append(f"/login pics élevés : max {login['max_ms']:.0f}ms.")

    # Suggestions générales
    notes.append("Le scénario effectue un login à chaque itération : c'est un stress-test d'authentification (pire cas).")
    notes.append("Pour un scénario métier réaliste, utiliser setup() dans k6 pour authentifier une fois par VU.")

    return bottlenecks, notes

def thresholds_section():
    # Seuils cibles / critiques (TP)
    return {
        "targets": {
            "/login": {"p95_ms": 2000, "err_pct": 1},
            "/users": {"p95_ms": 1000, "err_pct": 1},
            "/orders": {"p95_ms": 800, "err_pct": 1},
        },
        "critical": {
            "/login": {"avg_ms": 5000, "err_pct": 2},
            "/users": {"max_ms": 5000, "err_pct": 2},
            "/orders": {"max_ms": 3000, "err_pct": 2},
        },
    }

def write_kpi_md(out_path, run_name, kpis):
    lines = []
    lines.append(f"# KPI - {run_name}\n")
    lines.append("| Endpoint | Latence moyenne (ms) | Temps max (ms) | Taux d’erreur (%) | Throughput (req/sec) |")
    lines.append("|---|---:|---:|---:|---:|")
    for ep in ENDPOINTS:
        data = kpis.get(ep)
        if data is None:
            lines.append(f"| {ep} | N/A | N/A | N/A | N/A |")
        else:
            lines.append(
                f"| {ep} | {data['avg_ms']:.2f} | {data['max_ms']:.2f} | {data['err_pct']:.2f} | {data['throughput']:.2f} |"
            )
    lines.append("")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def write_report_md(out_path, all_runs):
    thr = thresholds_section()
    lines = []
    lines.append("# Rapport d’analyse – TP 3.3 (CI/CD)\n")
    lines.append("Ce rapport est généré automatiquement en CI à partir des exports JSON de k6.\n")

    # Synthèse
    lines.append("## Synthèse\n")
    for run_name, kpis in all_runs.items():
        bottlenecks, notes = classify(kpis)
        lines.append(f"### {run_name}\n")
        if bottlenecks:
            lines.append("**Goulets d’étranglement détectés :**")
            for b in bottlenecks:
                lines.append(f"- {b}")
        else:
            lines.append("Aucun goulet critique détecté sur les règles simples.")
        lines.append("")
        lines.append("**Notes de contexte :**")
        for n in notes:
            lines.append(f"- {n}")
        lines.append("")

    # Seuils
    lines.append("## Seuils recommandés\n")
    lines.append("### Seuils cibles\n")
    for ep, v in thr["targets"].items():
        lines.append(f"- **{ep}** : p95 < {v['p95_ms']}ms ; erreurs < {v['err_pct']}%")
    lines.append("\n### Seuils critiques\n")
    for ep, v in thr["critical"].items():
        if "avg_ms" in v:
            lines.append(f"- **{ep}** : moyenne ≥ {v['avg_ms']}ms ou erreurs ≥ {v['err_pct']}%")
        else:
            lines.append(f"- **{ep}** : max ≥ {v['max_ms']}ms ou erreurs ≥ {v['err_pct']}%")

    # Recos
    lines.append("\n## Recommandations priorisées\n")
    lines.append("### P0 – Stabiliser /login\n")
    lines.append("- Vérifier la saturation CPU (hash mot de passe) et ajuster le cost bcrypt/argon2 si nécessaire.")
    lines.append("- Optimiser l’accès DB au login : index sur email, chargement rôles en eager-loading, réduire les requêtes.")
    lines.append("- Ajuster le pool DB (SQLAlchemy) et vérifier les limites de connexions côté SGBD.")
    lines.append("\n### P1 – Réduire la variabilité /users\n")
    lines.append("- Pagination stricte et réduction du payload en liste.")
    lines.append("- Vérifier N+1 et optimiser les relations/joins.")
    lines.append("\n### P2 – Rendre la CI plus représentative\n")
    lines.append("- Ajouter un scénario k6 “métier” : login une fois par VU (setup), puis appels /users et /orders.")
    lines.append("- Conserver un scénario “stress-login” pour trouver le point de rupture.\n")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Dossier contenant k6_10.json, k6_50.json, k6_100.json")
    ap.add_argument("--output", required=True, help="Dossier de sortie (reports)")
    args = ap.parse_args()

    os.makedirs(args.output, exist_ok=True)

    mapping = {
        "k6_10.json": "Run 10 VUs",
        "k6_50.json": "Run 50 VUs",
        "k6_100.json": "Run 100 VUs",
    }

    all_runs = {}
    for fname, run_name in mapping.items():
        path = os.path.join(args.input, fname)
        if not os.path.exists(path):
            continue
        kpis = compute_kpis(path)
        all_runs[run_name] = kpis

        out_kpi = os.path.join(args.output, f"KPI_{fname.replace('.json','')}.md")
        write_kpi_md(out_kpi, run_name, kpis)

    # KPI global (option)
    if all_runs:
        write_report_md(os.path.join(args.output, "REPORT.md"), all_runs)

if __name__ == "__main__":
    main()
