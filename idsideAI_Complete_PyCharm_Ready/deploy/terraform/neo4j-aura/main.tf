terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = var.aws_region
}

# This module does not create the Aura instance (managed by Neo4j),
# but it provisions AWS Secrets for credentials and outputs values
# to be consumed by ECS/Render/Kubernetes deploys.

resource "aws_secretsmanager_secret" "neo4j_uri" { name = "${var.name}/neo4j/uri" }
resource "aws_secretsmanager_secret_version" "neo4j_uri_v" {
  secret_id = aws_secretsmanager_secret.neo4j_uri.id
  secret_string = var.neo4j_uri
}

resource "aws_secretsmanager_secret" "neo4j_user" { name = "${var.name}/neo4j/user" }
resource "aws_secretsmanager_secret_version" "neo4j_user_v" {
  secret_id = aws_secretsmanager_secret.neo4j_user.id
  secret_string = var.neo4j_user
}

resource "aws_secretsmanager_secret" "neo4j_password" { name = "${var.name}/neo4j/password" }
resource "aws_secretsmanager_secret_version" "neo4j_password_v" {
  secret_id = aws_secretsmanager_secret.neo4j_password.id
  secret_string = var.neo4j_password
}

output "neo4j_uri_secret_arn" { value = aws_secretsmanager_secret.neo4j_uri.arn }
output "neo4j_user_secret_arn" { value = aws_secretsmanager_secret.neo4j_user.arn }
output "neo4j_password_secret_arn" { value = aws_secretsmanager_secret.neo4j_password.arn }
