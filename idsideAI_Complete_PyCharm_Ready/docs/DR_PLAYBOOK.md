
# Disaster Recovery Playbook — IDECIDE

## Scope
- Neo4j Aura DB, Backend exports (/exports), Frontend static, Stripe billing state (source of truth in Stripe).

## Backups
- **Neo4j Aura**: enable daily automated backups (7/30/90 retention per tier).
- **Exports**: sync /exports to S3 with versioning + lifecycle policy (IA after 30d, Glacier after 180d).
- **Config**: Terraform state stored in remote backend (e.g., S3+DynamoDB).

## Recovery
1. Recreate infrastructure via Terraform (ECS/K8s + TLS/DNS modules).
2. Restore Aura snapshot from desired timestamp.
3. Restore /exports bucket to last known good version.
4. Recreate secrets (ESO/IRSA) and redeploy backend + frontend.
5. Validate health: /health, open app, run snapshot+compare, export Why/Audit.

## RPO/RTO
- Target RPO ≤ 24h (daily Aura backup) or ≤ 1h with PITR (if enabled).
- Target RTO ≤ 2h (infra as code + automated deploy).

## Runbook verification
- Quarterly DR drill: simulate loss, restore to staging, sign-off checklists.
