
import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  vus: 30,
  duration: '2m',
  thresholds: {
    http_req_duration: ['p(95)<300'],
    http_req_failed: ['rate<0.01'],
  },
};

const API = __ENV.API || 'http://localhost:8001';

export default function () {
  const health = http.get(`${API}/health`);
  check(health, {'health ok': (r)=> r.status===200});
  const sub = http.get(`${API}/graphs/demo/subgraph`);
  check(sub, {'subgraph ok': (r)=> r.status===200});
  const diff = http.get(`${API}/graphs/demo/diff?frm=v1&to=v2`);
  check(diff, {'diff ok': (r)=> r.status===200});
  sleep(1);
}
