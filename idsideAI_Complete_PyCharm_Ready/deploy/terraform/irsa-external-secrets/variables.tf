
variable "name" { type = string }
variable "aws_region" { type = string }
variable "namespace" { type = string }
variable "service_account_name" { type = string }
variable "allowed_secret_arns" { type = list(string) }
variable "cluster_oidc_provider_arn" { type = string }
variable "cluster_oidc_provider_url" { type = string
  description = "The issuer URL without https:// (e.g., oidc.eks.eu-west-1.amazonaws.com/id/XXXX)"
}
