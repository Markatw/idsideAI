
output "frontend_url" { value = "http://${aws_lb.this.dns_name}" }
output "api_base" { value = "http://${aws_lb.this.dns_name}" }
