variable "name" { type = string }
variable "aws_region" { type = string, default = "eu-west-1" }
variable "neo4j_uri" { type = string, description = "neo4j+s://<your-aura-endpoint>" }
variable "neo4j_user" { type = string, description = "Neo4j username" }
variable "neo4j_password" { type = string, sensitive = true, description = "Neo4j password" }
