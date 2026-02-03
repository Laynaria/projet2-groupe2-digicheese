#!/usr/bin/env python3
"""
Script pour parser les résultats JSON de k6 et générer un rapport markdown.
Usage: python parse_k6.py --input performance/results --output reports
"""

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List, Any


def parse_k6_json(filepath: Path) -> Dict[str, Any]:
    """Parse un fichier JSON k6 et extrait les métriques importantes."""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()

        # Dernière ligne contient le summary
        if not lines:
            return {}

        # k6 écrit plusieurs lignes JSON, on cherche les métriques
        metrics = {
            'http_reqs': {},
            'http_req_duration': {},
            'http_req_failed': {},
            'vus': {},
            'iterations': {}
        }

        for line in lines:
            try:
                data = json.loads(line)
                metric_name = data.get('metric')

                if metric_name in metrics:
                    if 'data' in data:
                        metrics[metric_name] = data['data']
            except json.JSONDecodeError:
                continue

        return metrics
    except Exception as e:
        print(f"⚠️  Erreur lors du parsing de {filepath}: {e}")
        return {}


def parse_k6_summary(filepath: Path) -> Dict[str, Any]:
    """Parse le fichier summary JSON exporté par k6."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Erreur lors du parsing du summary {filepath}: {e}")
        return {}


def format_duration(ms: float) -> str:
    """Formate une durée en millisecondes."""
    if ms < 1:
        return f"{ms:.2f}ms"
    elif ms < 1000:
        return f"{ms:.0f}ms"
    else:
        return f"{ms / 1000:.2f}s"


def format_rate(rate: float) -> str:
    """Formate un taux."""
    return f"{rate:.2f}/s"


def generate_report(results_dir: Path, output_dir: Path) -> None:
    """Génère un rapport markdown à partir des résultats k6."""

    output_dir.mkdir(parents=True, exist_ok=True)

    # Chercher tous les fichiers summary
    summaries = {}
    for file in results_dir.glob("summary_*.json"):
        vus = file.stem.replace("summary_", "")
        summary = parse_k6_summary(file)
        if summary:
            summaries[vus] = summary

    # Si pas de summary, essayer de parser les fichiers JSON bruts
    if not summaries:
        for file in results_dir.glob("k6_*.json"):
            vus = file.stem.replace("k6_", "")
            metrics = parse_k6_json(file)
            if metrics:
                summaries[vus] = {"metrics": metrics}

    # Générer le rapport
    report_path = output_dir / "REPORT.md"

    with open(report_path, 'w') as f:
        f.write("# 📊 Performance Test Results (k6)\n\n")

        if not summaries:
            f.write("⚠️  No results found. Check that k6 tests ran successfully.\n")
            return

        f.write(f"**Generated:** {Path.cwd()}\n\n")
        f.write("## 📈 Test Scenarios\n\n")

        # Tableau comparatif
        f.write("| Scenario | Requests | Success Rate | Avg Duration | P95 Duration | Max Duration |\n")
        f.write("|----------|----------|--------------|--------------|--------------|-------------|\n")

        for vus in sorted(summaries.keys(), key=lambda x: int(x)):
            summary = summaries[vus]
            metrics = summary.get('metrics', {})

            # Extraire les métriques
            http_reqs = metrics.get('http_reqs', {})
            http_req_duration = metrics.get('http_req_duration', {})
            http_req_failed = metrics.get('http_req_failed', {})

            # Calculer les valeurs
            total_reqs = http_reqs.get('count', 0)

            # Taux de succès
            failed_count = http_req_failed.get('count', 0)
            failed_rate = http_req_failed.get('rate', 0) if http_req_failed else 0
            success_rate = (1 - failed_rate) * 100 if failed_rate else 100

            # Durées
            avg_duration = http_req_duration.get('avg', 0)
            p95_duration = http_req_duration.get('p(95)', 0)
            max_duration = http_req_duration.get('max', 0)

            # Écrire la ligne
            f.write(f"| **{vus} VUs** | {total_reqs:,} | {success_rate:.1f}% | "
                    f"{format_duration(avg_duration)} | {format_duration(p95_duration)} | "
                    f"{format_duration(max_duration)} |\n")

        f.write("\n## 📋 Detailed Results\n\n")

        # Détails par scénario
        for vus in sorted(summaries.keys(), key=lambda x: int(x)):
            summary = summaries[vus]
            metrics = summary.get('metrics', {})

            f.write(f"### {vus} VUs\n\n")

            # HTTP Requests
            http_reqs = metrics.get('http_reqs', {})
            if http_reqs:
                total = http_reqs.get('count', 0)
                rate = http_reqs.get('rate', 0)
                f.write(f"**Total Requests:** {total:,} ({format_rate(rate)})\n\n")

            # Request Duration
            http_req_duration = metrics.get('http_req_duration', {})
            if http_req_duration:
                f.write("**Request Duration:**\n")
                f.write(f"- Average: {format_duration(http_req_duration.get('avg', 0))}\n")
                f.write(f"- Median: {format_duration(http_req_duration.get('med', 0))}\n")
                f.write(f"- P95: {format_duration(http_req_duration.get('p(95)', 0))}\n")
                f.write(f"- P99: {format_duration(http_req_duration.get('p(99)', 0))}\n")
                f.write(f"- Max: {format_duration(http_req_duration.get('max', 0))}\n\n")

            # Failures
            http_req_failed = metrics.get('http_req_failed', {})
            if http_req_failed:
                failed_count = http_req_failed.get('count', 0)
                failed_rate = http_req_failed.get('rate', 0)

                if failed_count > 0:
                    f.write(f"**⚠️ Failures:** {failed_count} ({failed_rate * 100:.2f}%)\n\n")
                else:
                    f.write("**✅ No failures**\n\n")

            # Iterations
            iterations = metrics.get('iterations', {})
            if iterations:
                iter_count = iterations.get('count', 0)
                iter_rate = iterations.get('rate', 0)
                f.write(f"**Iterations:** {iter_count:,} ({format_rate(iter_rate)})\n\n")

            f.write("---\n\n")

        f.write("## 🎯 Recommendations\n\n")

        # Analyser les résultats et donner des recommandations
        all_vus = sorted(summaries.keys(), key=lambda x: int(x))
        if len(all_vus) > 1:
            first_vus = summaries[all_vus[0]].get('metrics', {})
            last_vus = summaries[all_vus[-1]].get('metrics', {})

            first_avg = first_vus.get('http_req_duration', {}).get('avg', 0)
            last_avg = last_vus.get('http_req_duration', {}).get('avg', 0)

            if last_avg > first_avg * 2:
                f.write("- ⚠️  **Performance degradation detected** under high load\n")
                f.write("- Consider optimizing database queries or adding caching\n")
                f.write("- Review connection pool settings\n\n")
            else:
                f.write("- ✅ **Good scalability** - performance remains stable under load\n\n")

        # Vérifier les taux d'erreur
        for vus, summary in summaries.items():
            failed = summary.get('metrics', {}).get('http_req_failed', {})
            if failed.get('count', 0) > 0:
                f.write(f"- ⚠️  **{vus} VUs**: {failed.get('count', 0)} failures detected - investigate error logs\n")

        f.write("\n## 📦 Artifacts\n\n")
        f.write("Detailed JSON results are available in the artifacts for further analysis.\n")

    print(f"✅ Report generated: {report_path}")


def main():
    parser = argparse.ArgumentParser(description='Parse k6 results and generate KPI report')
    parser.add_argument('--input', required=True, help='Input directory with k6 JSON results')
    parser.add_argument('--output', required=True, help='Output directory for reports')

    args = parser.parse_args()

    results_dir = Path(args.input)
    output_dir = Path(args.output)

    if not results_dir.exists():
        print(f"❌ Input directory not found: {results_dir}")
        return 1

    generate_report(results_dir, output_dir)
    return 0


if __name__ == '__main__':
    exit(main())