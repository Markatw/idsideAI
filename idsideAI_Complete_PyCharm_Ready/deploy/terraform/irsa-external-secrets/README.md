
# IRSA for External Secrets (AWS Secrets Manager)

Creates an IAM role that the Kubernetes ServiceAccount for External Secrets Operator (or your app)
can assume via IRSA to read **specific** Secrets Manager ARNs.

## Inputs
- `name`: logical name (e.g., idecide-prod)
- `aws_region`: e.g., eu-west-1
- `namespace`: Kubernetes namespace where the ServiceAccount lives
- `service_account_name`: name of the ServiceAccount
- `allowed_secret_arns`: list of secret ARNs the role may read
- `cluster_oidc_provider_arn`: ARN of the EKS cluster OIDC provider
- `cluster_oidc_provider_url`: issuer URL *without* https:// (e.g., oidc.eks.eu-west-1.amazonaws.com/id/XXXX)

## Output
- `role_arn` — annotate your ServiceAccount:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: idecide-backend
  namespace: idecide
  annotations:
    eks.amazonaws.com/role-arn: <role_arn>
```
