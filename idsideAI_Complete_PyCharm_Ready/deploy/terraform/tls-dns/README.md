
# TLS + DNS (Terraform)

- Provisions an ACM certificate for your apex/root domain
- Creates Route53 validation records
- Points the domain A-record at your ALB (from ECS module outputs)

## Usage
```hcl
module "tls_dns" {
  source       = "./deploy/terraform/tls-dns"
  aws_region   = "eu-west-1"
  domain       = "app.yourdomain.com"
  zone_id      = "Z123..."
  alb_dns_name = module.ecs.alb_dns_name
  alb_zone_id  = module.ecs.alb_zone_id
}
```
Apply, then update your ECS ALB listener to use `module.tls_dns.certificate_arn`.
