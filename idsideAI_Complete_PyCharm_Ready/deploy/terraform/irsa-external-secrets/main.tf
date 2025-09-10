
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current" {}

# IAM policy allowing access to specific Secrets Manager ARNs
data "aws_iam_policy_document" "secrets_access" {
  statement {
    effect = "Allow"
    actions = [
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret"
    ]
    resources = var.allowed_secret_arns
  }
}

resource "aws_iam_policy" "secrets_policy" {
  name        = "${var.name}-secrets-access"
  description = "Allow ESO to read specific secrets for ${var.name}"
  policy      = data.aws_iam_policy_document.secrets_access.json
}

# Trust policy for IRSA
data "aws_iam_policy_document" "assume_role" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    principals {
      type        = "Federated"
      identifiers = [var.cluster_oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "${var.cluster_oidc_provider_url}:sub"
      values   = ["system:serviceaccount:${var.namespace}:${var.service_account_name}"]
    }

    condition {
      test     = "StringEquals"
      variable = "${var.cluster_oidc_provider_url}:aud"
      values   = ["sts.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "irsa_role" {
  name               = "${var.name}-irsa-external-secrets"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy_attachment" "attach" {
  role       = aws_iam_role.irsa_role.name
  policy_arn = aws_iam_policy.secrets_policy.arn
}

output "role_arn" { value = aws_iam_role.irsa_role.arn }
