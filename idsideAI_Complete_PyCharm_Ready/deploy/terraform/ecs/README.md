
# IDECIDE Terraform ECS Module

Deploys IDECIDE frontend (static, port 80) and backend (FastAPI, port 8001) on **AWS ECS Fargate** behind an **ALB**.
Assumes an existing **VPC** with **public** and **private** subnets.

## Usage
```hcl
module "idecide" {
  source              = "./deploy/terraform/ecs"
  name                = "idecide-prod"
  region              = "eu-west-1"
  vpc_id              = "vpc-123456"
  public_subnet_ids   = ["subnet-aaa","subnet-bbb"]
  private_subnet_ids  = ["subnet-ccc","subnet-ddd"]

  backend_image       = "ghcr.io/you/idecide-backend:latest"
  frontend_image      = "ghcr.io/you/idecide-frontend:latest"

  neo4j_uri           = "bolt://your-neo4j:7687"
  neo4j_user          = "neo4j"
  neo4j_password      = "changeme"

  jwks_url            = "https://your-auth/.well-known/jwks.json"
  jwt_audience        = "your-aud"
  jwt_issuer          = "https://your-auth/"
  stripe_secret_key   = "sk_live_xxx"
  stripe_webhook_secret = "whsec_xxx"

  tags = { Environment = "prod" }
}
```

Outputs:
- `frontend_url` — UI address
- `api_base` — backend base (same ALB hostname)
