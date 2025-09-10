# IDECIDE Graph API (Neo4j)

## Setup
```bash
cd backend
cp .env.example .env
# edit NEO4J_*
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8001
```

## Neo4j constraints & seed
Run the Cypher in `db/migrations.cypher` in your Neo4j Browser, then call:
- GET /graphs/{graph_id}/subgraph?root=DEC-1
- GET /graphs/{graph_id}/snapshots
- GET /graphs/{graph_id}/diff?from=v1&to=v2


## Auth via JWKS
Set in `.env`:
```
JWKS_URL=https://your-domain/.well-known/jwks.json
JWT_AUDIENCE=your-audience
JWT_ISSUER=https://your-domain/
JWT_ALGORITHMS=RS256
```
`GET /whoami` returns decoded claims when Authorization header is provided.
