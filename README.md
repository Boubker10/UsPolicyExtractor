
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
