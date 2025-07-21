
# Deployment Guide: AWS ECR and EC2 for UsPolicyExtractor

This guide explains how to build and push your Docker image to AWS Elastic Container Registry (ECR), and then run/test the container on an AWS EC2 instance.

---

## Prerequisites

- AWS CLI installed and configured with appropriate permissions (`ecr`, `ec2`, etc.)
- Docker installed locally or on EC2 instance
- An AWS account with access to ECR and EC2
- AWS IAM permissions for ECR push/pull and EC2 usage

---

## Step 1: Build Docker Image Locally

```bash
docker build -t legal-ocr-agent .

```

## Step 2: Authenticate Docker to AWS ECR

```bash
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <account_id>.dkr.ecr.<your-region>.amazonaws.com
```

##  Step 3: Tag Docker Image for ECR

```bash 
docker tag legal-ocr-agent:latest <account_id>.dkr.ecr.<your-region>.amazonaws.com/legal-ocr-agent:latest
```

## Step 4: Push Docker Image to AWS ECR

```bash
docker push <account_id>.dkr.ecr.<your-region>.amazonaws.com/legal-ocr-agent:latest
```

# 2. Run Docker Container on AWS EC2

## Step 1: Launch an EC2 Instance

- **AMI**: Amazon Linux 2023
- **Instance type**: t3.medium (or one fitting your capacity needs)
- **Security Group**: Allow inbound SSH (port 22) and all required ports for your application (e.g., 9000).

## Step 2: Connect to Your EC2 Instance

ssh -i your-key.pem ec2-user@your-ec2-public-ip

text

## Step 3: Install Docker on EC2
```bash
sudo dnf install -y docker
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker ec2-user
newgrp docker
```
You may need to log out and log back in for group changes to apply[2][3].

## Step 4: Authenticate Docker with ECR on EC2
```bash
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <account_id>.dkr.ecr.<your-region>.amazonaws.com
```

## Step 5: Pull and Run Your Docker Image on EC2

```bash
docker pull <account_id>.dkr.ecr.<your-region>.amazonaws.com/legal-ocr-agent:latest

docker run -p 9000:8080 <account_id>.dkr.ecr.<your-region>.amazonaws.com/legal-ocr-agent:latest
```
> **Adjust ports as necessary for your application.**  
Verify your security group allows incoming traffic on the mapped port[3][5].

---

## 3. Test Your Lambda Container Locally (Optional)

If your container exposes a Lambda-compatible API:
```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"body": "{"question": "What is the export law in Texas?"}"}'

```

---

## 4. Automate Build and Push with GitHub Actions

Create a `.github/workflows/deploy.yml` file:

```bash
name: Test and Deploy to AWS ECR

on:
push:
branches:
- main

jobs:
build-and-push:
runs-on: ubuntu-latest

text
steps:
  - name: Checkout code
    uses: actions/checkout@v3

  - name: Set up Docker Buildx
    uses: docker/setup-buildx-action@v2

  - name: Log in to Amazon ECR
    uses: aws-actions/amazon-ecr-login@v1

  - name: Build and push Docker image
    uses: docker/build-push-action@v3
    with:
      context: .
      push: true
      tags: ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.${{ secrets.AWS_REGION }}.amazonaws.com/legal-ocr-agent:latest

  - name: Notify failure on Discord
    if: failure()
    uses: Ilshidur/action-discord@master
    with:
      webhook: ${{ secrets.DISCORD_WEBHOOK }}
      message: |
        ❌ Deployment failed for `${{ github.repository }}` on branch `${{ github.ref_name }}`
        Author: `${{ github.actor }}`
        See logs: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

**Configure these GitHub secrets:**

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `AWS_ACCOUNT_ID`
- `DISCORD_WEBHOOK` (*optional*)



