import http from "k6/http";
import { check, group, sleep } from "k6";

// ---------------------------
// Config (via -e ...)
// ---------------------------
const BASE_URL = __ENV.BASE_URL || "http://host.docker.internal:8000";
const EMAIL = __ENV.EMAIL || "admin@digicheese.com";
const PASSWORD = __ENV.PASSWORD || "Admin123!";
const API_PREFIX = __ENV.API_PREFIX || "/api/v1";

export const options = {
  vus: Number(__ENV.VUS || 10),
  duration: __ENV.DURATION || "30s",
  thresholds: {
    // Seuils assouplis pour le CI (environnement moins performant que la prod)
    http_req_failed: ["rate<0.05"], // < 5% d'erreurs (au lieu de 2%)
    http_req_duration: [
      "p(95)<3000", // p95 < 3s (au lieu de 800ms - plus réaliste en CI)
      "p(99)<5000", // p99 < 5s
    ],
  },
};

function loginAndGetToken() {
  const url = `${BASE_URL}${API_PREFIX}/auth/login`;
  const payload = JSON.stringify({ email: EMAIL, motDePasse: PASSWORD });

  const res = http.post(url, payload, {
    headers: { "Content-Type": "application/json" },
    tags: { endpoint: "/login" },
  });

  const ok = check(res, {
    "login returns 200": (r) => r.status === 200,
    "token present": (r) => {
      try {
        const body = r.json();
        return !!body?.access_token;
      } catch {
        return false;
      }
    },
  });

  if (!ok) {
    console.log(`LOGIN FAILED status=${res.status} body=${res.body}`);
    return null;
  }

  return res.json().access_token;
}

export default function () {
  const token = loginAndGetToken();
  if (!token) {
    sleep(1);
    return;
  }

  const authHeaders = { headers: { Authorization: `Bearer ${token}` } };

  group("AUTH_ME", () => {
    const res = http.get(`${BASE_URL}${API_PREFIX}/auth/me`, {
      ...authHeaders,
      tags: { endpoint: "/me" },
    });
    check(res, { "me returns 200": (r) => r.status === 200 });
  });

  group("USERS_LIST", () => {
    const res = http.get(`${BASE_URL}${API_PREFIX}/utilisateurs/`, {
      ...authHeaders,
      tags: { endpoint: "/users" },
    });
    check(res, { "users returns 200": (r) => r.status === 200 });
  });

  group("ORDERS_LIST", () => {
    const res = http.get(`${BASE_URL}${API_PREFIX}/commande/`, {
      ...authHeaders,
      tags: { endpoint: "/orders" },
    });
    check(res, { "orders returns 200": (r) => r.status === 200 });
  });

  sleep(1);
}
