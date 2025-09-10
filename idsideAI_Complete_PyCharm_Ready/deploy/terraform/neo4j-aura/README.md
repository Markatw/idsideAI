# Neo4j Aura — Terraform Secrets Module

> Aura instances are provisioned in the Neo4j Cloud Console. This module **does not** create an Aura DB; it provisions **AWS Secrets Manager** entries for the **URI**, **user**, and **password**, so your ECS/Kubernetes/Render deployments can consume them safely.

## Usage

```hcl
module "aura" {
  source        = "./deploy/terraform/neo4j-aura"
  name          = "idsideai-prod"
  aws_region    = "eu-west-1"
  neo4j_uri     = "neo4j+s://<your-aura-endpoint>"
  neo4j_user    = "neo4j"
  neo4j_password= var.neo4j_password
}
```

Outputs:
- `neo4j_uri_secret_arn`
- `neo4j_user_secret_arn`
- `neo4j_password_secret_arn`

Wire these into your ECS TaskDefinition or Kubernetes Secret to set:
- `NEO4J_URI`
- `NEO4J_USER`
- `NEO4J_PASSWORD`
