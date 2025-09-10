# AWS ECS/Fargate Quick Deploy (Blueprint)

This folder includes a minimal blueprint to deploy the frontend and backend to ECS Fargate.
Steps:
1) Build & push images to ECR (scripts not included here).
2) Use the provided task definitions to create services.
3) Supply environment variables (NEO4J_URI, JWKS_URL, etc.) via SSM Parameter Store or Secrets Manager.
