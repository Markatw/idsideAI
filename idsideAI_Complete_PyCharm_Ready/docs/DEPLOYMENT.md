# Deployment

## Docker Compose
- `docker compose up -d` brings up Neo4j, backend (8001), frontend (5173).
- Add observability with `docker compose -f docker-compose.yml -f docker-compose.observability.yml up -d`.

## Kubernetes
- Apply manifests in `k8s/` (edit images and secrets).
- Use NGINX Ingress per `ingress.yml`.
