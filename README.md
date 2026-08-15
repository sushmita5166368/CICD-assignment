## Steps involved in Creating the CICD pipeline for this App
Step1 :Create a Simple Flask app and Push in github
Step2 :Create Docker file and pytest suite 
Step3 :Create ECR repository and EC2 and apply the IAM rule 
Step4 :Create A IAM user and assign the required roles
Step5 :Create  PIPELINE for Pushing docker image on ECR
Step6 :From ECR the image will be pushed to EC2 and create a container 
Step7 :Notify over email for every push of ECR image to EC2

## Prerequisites
# AWS services access
-> EC2 instances with proper IAM role and network connectivity along with private key
-> Should allow the port 22 for SSH configuration
-> ECR Repository 
-> IAM user who must have proper role assigned and access keys

## To configure the pipeline's required secrets
-> ADD Aws credentials on Secrets (access and secret access key)
-> EC2 host IP/DNS and private key
-> SMTP address and setting involved  sender user address and credentials

## EC2 Connection Strategy

### Connection Method: SSH

#### Technical Workflow
1. The deployment job retrieves `EC2_HOST`, `EC2_USERNAME`, and `SSH_PRIVATE_KEY` securely from CI/CD Secrets.
2. The pipeline initiates an SSH session to port 22 on the target EC2 instance.
3. Upon authentication, the pipeline executes the deployment sequence directly on the host:
   - Logs into Amazon ECR (`aws ecr get-login-password`).
   - Pulls the specific application image tag matching the Git commit SHA.
   - Stops and removes any pre-existing app container instance.
   - Starts the new container on the designated host port.
   - Executes a health-check request (`curl -f http://localhost:<PORT>/health`) to verify container stability.

#### Rationale for Selection
SSH was chosen over AWS SSM primarily for convenience, setup speed, and simplicity:
- **Zero Agent Dependency:** Requires no additional AWS Systems Manager configuration or complex IAM instance profiles to manage remote execution permissions.
- **Immediate Setup:** Leverages standard key-pair authentication and native SSH tooling already embedded within CI/CD runner environments.
- **Portability:** Offers straightforward, uniform command execution across diverse build platforms without platform-specific SDK dependencies.

## Manual Deployment Fallback Procedure

If the CI/CD pipeline (Jenkins / GitHub Actions) is unavailable, follow these steps to manually deploy the application to the EC2 instance:

### Step 1: Build & Push Image from Local Machine
Execute the following commands in your local application repository:
```bash
# Get current commit SHA
export COMMIT_SHA=$(git rev-parse --short HEAD)
export AWS_ACCOUNT_ID="<YOUR_AWS_ACCOUNT_ID>"
export AWS_REGION="<YOUR_AWS_REGION>"
export ECR_REPO="<YOUR_ECR_REPOSITORY_NAME>"
export IMAGE_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}[.amazonaws.com/$](https://.amazonaws.com/$){ECR_REPO}:${COMMIT_SHA}"

# Build and push to ECR
docker build -t $IMAGE_URI .
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
docker push $IMAGE_URI



