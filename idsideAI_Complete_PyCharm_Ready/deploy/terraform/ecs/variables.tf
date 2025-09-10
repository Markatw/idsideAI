
variable "name" { type = string }
variable "region" { type = string }
variable "vpc_id" { type = string }
variable "public_subnet_ids" { type = list(string) }
variable "private_subnet_ids" { type = list(string) }
variable "backend_image" { type = string }
variable "frontend_image" { type = string }
variable "backend_cpu" { type = string default = "512" }
variable "backend_memory" { type = string default = "1024" }
variable "frontend_cpu" { type = string default = "256" }
variable "frontend_memory" { type = string default = "512" }
variable "backend_desired_count" { type = number default = 1 }
variable "frontend_desired_count" { type = number default = 1 }
variable "log_retention_days" { type = number default = 7 }
variable "neo4j_uri" { type = string }
variable "neo4j_user" { type = string }
variable "neo4j_password" { type = string }
variable "jwks_url" { type = string }
variable "jwt_audience" { type = string }
variable "jwt_issuer" { type = string }
variable "stripe_secret_key" { type = string }
variable "stripe_webhook_secret" { type = string }
variable "tags" { type = map(string) default = {} }
