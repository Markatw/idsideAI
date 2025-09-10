# IDECIDE Auth & Security

- Supports **JWT Bearer** auth with optional JWKS (OIDC) verification.
- Tenant isolation via `X-Tenant` / `X-Workspace` headers (middleware extracts and passes to queries).
- Secrets are injected via environment variables.
- **Do not** use unverified tokens in production — configure JWKS or HS256 secret.

## OIDC/SSO
Configure JWKS via `JWKS_URL` or set `JWT_SECRET/JWT_ISSUER/JWT_AUDIENCE` for HS256.
