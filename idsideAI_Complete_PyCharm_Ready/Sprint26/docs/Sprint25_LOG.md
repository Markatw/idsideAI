# Sprint 25 — Running Log (protocol v2)

## 25.1 — Scaffold & baseline carryover
- Time: 03-09-2025 09:03 (Europe/London)
- Actions: Created Sprint25 root; VERSION set to 25.0.0; initialized log.

## 25.2 — SCIM API stub (user provisioning)
- Time: 03-09-2025 09:06 (Europe/London)
- utils/scim: user_skeleton(), list_response()
- routes/scim: ServiceProviderConfig, Users list/create/patch/delete

## 25.3 — SSO login hooks (SAML/OIDC)
- Time: 03-09-2025 09:07 (Europe/London)
- utils/sso: saml_metadata(), oidc_discovery(), test_login()
- routes/sso: SAML metadata XML, OIDC discovery, test login

## 25.4 — PII encryption helper R2
- Time: 03-09-2025 09:09 (Europe/London)
- utils/pii_crypto: encrypt_pii(), decrypt_pii() demo-only keystream XOR
- routes/pii_crypto: /api/crypto/pii/encrypt, /decrypt

## 25.5 — DB encryption at rest config
- Time: 03-09-2025 09:11 (Europe/London)
- utils/db_crypto: get_db_key(), wrap_sqlite_conn()
- routes/db_crypto: /status, /setkey

## 25.6 — Backup/restore scripts (DR R2)
- Time: 03-09-2025 10:19 (Europe/London)
- utils/dr_backup: backup_sqlite(), restore_sqlite()
- routes/dr: /api/dr/backup, /api/dr/restore

## 25.7 — Prometheus metrics (health & latency)
- Time: 03-09-2025 10:21 (Europe/London)
- utils/metrics: counters + histograms + render_prometheus()
- routes/metrics: /health, /probe, /prometheus

## 25.8 — Logging enrichment (structured JSON)
- Time: 03-09-2025 10:22 (Europe/London)
- utils/logging: JSON logger
- routes/log_test: /api/log/test

## 25.9 — Pre-wrap stabilization
- Time: 03-09-2025 10:23 (Europe/London)
- VERSION bumped to 25.0.1
- Ensured imports + __init__.py presence

## 25.10 — Deep Audit Pack + Wrap
- Time: 03-09-2025 10:27 (Europe/London)
- Generated full manifest, critical hashes, stub sweep, delta summary
