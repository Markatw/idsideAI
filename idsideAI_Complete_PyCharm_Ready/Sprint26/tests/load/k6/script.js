import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  vus: __ENV.VUS ? parseInt(__ENV.VUS) : 5,
  duration: __ENV.DURATION || '30s',
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% below 500ms
    http_req_failed: ['rate<0.01'],   // <1% errors
  },
};

const BASE = __ENV.BASE || 'http://localhost:8000';

export default function () {
  const res = http.get(`${BASE}/api/metrics/health`);
  sleep(0.2);
}
