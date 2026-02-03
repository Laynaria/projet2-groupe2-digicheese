import http from "k6/http";
import { sleep, check } from "k6";

export const options = {
  vus: 10,
  duration: "30s",
  thresholds: {
    http_req_failed: ["rate<0.01"],        // < 1 % d’erreurs
    http_req_duration: ["p(95)<5000"],     // 95 % < 5 s
  },
};


// Variables d’environnement (k6)
const BASE_URL = __ENV.BASE_URL;
const EMAIL = __ENV.EMAIL;
const PASSWORD = __ENV.PASSWORD;

export default function () {
  // Sécurité minimale : éviter un test invalide
  if (!BASE_URL || !EMAIL || !PASSWORD) {
    throw new Error("BASE_URL, EMAIL ou PASSWORD non définis");
  }

  // 1) LOGIN
  const loginRes = http.post(
    `${BASE_URL}/api/v1/auth/login`,
    JSON.stringify({
      email: EMAIL,
      motDePasse: PASSWORD,
    }),
    { headers: { "Content-Type": "application/json" } }
  );

  check(loginRes, {
    "POST /auth/login -> 200": (r) => r.status === 200,
  });

  const token = loginRes.json("access_token");
  check(token, {
    "token présent": (t) => !!t,
  });

  if (!token) {
    sleep(1);
    return;
  }

  const authHeaders = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  // 2) /utilisateurs
  const usersRes = http.get(`${BASE_URL}/api/v1/utilisateurs/`, authHeaders);
  check(usersRes, {
    "GET /utilisateurs -> 200": (r) => r.status === 200,
  });

  // 3) /commande
  const cmdRes = http.get(`${BASE_URL}/api/v1/commande/`, authHeaders);
  check(cmdRes, {
    "GET /commande -> 200": (r) => r.status === 200,
  });

  sleep(1);
}
