# Calculator API with Web Interface

A simple calculator application built with Flask API backend and Nginx frontend, containerized with Docker and deployed on AWS ECS using CodeBuild for CI/CD

## 🏗️ Architecture

```
Internet → Load Balancer → ECS Service
                           ├── Flask API (Port 8000)
                           └── Nginx Web Server (Port 3000)
```

## 🚀 Live Demo

Access the calculator: `http://your-alb-dns-name:3000`

## 📁 Project Structure

```
calculator-app/
├── app.py                 # Flask API backend
├── index.html            # Web frontend
├── Dockerfile.api        # Flask container config
├── Dockerfile.web        # Nginx container config
├── docker-compose.yml    # Local development
└── README.md
```

## 🛠️ Technology Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML/JavaScript
- **Web Server:** Nginx
- **Containerization:** Docker
- **Cloud Platform:** AWS
- **Container Orchestration:** ECS Fargate
- **Load Balancer:** Application Load Balancer
- **Container Registry:** ECR

## 🏃‍♂️ Quick Start

### Local Development

```bash
# Clone repository
git clone <your-repo-url>
cd calculator-app

# Run with Docker Compose
docker-compose up --build

# Access application
# Web Interface: http://localhost:3000
# API Endpoint: http://localhost:8000
```

## ☁️ AWS Deployment

### Prerequisites

- AWS CLI installed and configured
- Docker installed
- AWS account with appropriate permissions

### Deployment Steps

### Step 1: Create ECR Repositories on AWS

### Step 2: Login and push images to ECR
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag for ECR
docker tag api-calculator-flask-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/api-calculator-flask-api:latest
docker tag api-calculator-web-server:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/api-calculator-web-server:latest

# Push to ECR
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/api-calculator-flask-api:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/api-calculator-web-server:latest
```

### Step 3: Create ECS Cluster

1. Go to **AWS ECS Console**
2. Click **"Create Cluster"**
3. Choose **"Fargate"**
4. Configure cluster settings and create

### Step 4: Create CodeBuild Project

1. Go to **AWS CodeBuild Console**
2. Click **"Create build project"**
3. Configure project:
   - **Project name**: `calculator-app-build`
   - **Source provider**: GitHub
   - **Repository**: Connect to your GitHub repository
   - **Environment**: 
     - **Runtime**: Standard
     - **Image**: `aws/codebuild/standard:5.0`
     - **Privileged**: ✅ (Required for Docker)
   - **Service role**: `codebuild-calculator-service-role`

4. **Environment Variables**:
   - `AWS_DEFAULT_REGION`
   - `FLASK_IMAGE_REPO_NAME`
   - `WEB_IMAGE_REPO_NAME`
   - `AWS_ACCOUNT_ID`
   - `IMAGE_TAG`
  
5. **Add Permission for** `codebuild-calculator-service-role` - `AmazonEC2ContainerRegistryPowerUser`:

### Step 5: Create ECS Cluster

1. Go to **"Task Definitions"** → **"Create new Task Definition"**
2. Choose **"Fargate"** based on your cluster
3. Configure task settings:
   - **Task Definition Name**: `calculator-app-task`
   - **Task Role**: Create or select appropriate role
   - **Task Memory**: 1GB
   - **Task CPU**: 0.5 vCPU

4. **Add Container Definitions**:
   
   **Container 1 - Flask API**:
   - **Container Name**: `flask-api`
   - **Image**: `<account-id>.dkr.ecr.us-east-1.amazonaws.com/api-calculator-flask-api:latest`
   - **Port Mappings**: `8000:8000`
   
   **Container 2 - Web Server**:
   - **Container Name**: `web-server`
   - **Image**: `<account-id>.dkr.ecr.us-east-1.amazonaws.com/api-calculator-web-server:latest`
   - **Port Mappings**: `3000:3000`

### Step 6: Create Security Group

1. Go to **EC2 Console** → **"Security Groups"**
2. Create new security group: `calculator-app-sg`
3. **Inbound Rules**:
   - Type: Custom TCP, Port: 3000, Source: 0.0.0.0/0
   - Type: Custom TCP, Port: 8000, Source: 0.0.0.0/0

### Step 7: Create ECS Service

1. Go to **ECS Cluster** → **"Create Service"**
2. Configure service:
   - **Launch Type**: Fargate
   - **Task Definition**: `calculator-app-task:1`
   - **Service Name**: `calculator-app-service`
   - **Number of Tasks**: 1

3. **Configure Network**:
   - **VPC**: Default VPC
   - **Subnets**: Select public subnets
   - **Security Group**: `calculator-app-sg`
   - **Auto-assign Public IP**: Enabled

4. **Load Balancing** (Optional but Recommended):
   - **Load Balancer Type**: Application Load Balancer
   - **Container**: `web-server 3000:3000`
   - **Listener Port**: 3000
   - **Target Group**: Create new

### Step 8: Access Your Application

1. Go to **ECS Service** → **"Configuration and Networking"** tab
2. Find the **Load Balancer DNS name** or **Public IP**
3. Access your application:
   - **Web Interface**: `http://<load-balancer-dns>:3000`
   - **API Endpoint**: `http://<load-balancer-dns>:8000`

## 📊 Usage Examples

### Web Interface
Visit the web interface and use the calculator form to perform operations.

## 📈 Monitoring and Scaling

### CloudWatch Integration
- ECS automatically sends metrics to CloudWatch
- Monitor CPU, Memory, and Network utilization
- Set up alarms for automated scaling

### Auto Scaling
Configure ECS Service Auto Scaling based on:
- CPU utilization
- Memory utilization
- Request count

## 🛡️ Security Considerations

- **API Security**: Implement authentication for production use
- **CORS**: Configure appropriate CORS settings
- **Security Groups**: Restrict access to necessary ports only
- **SSL/TLS**: Use HTTPS in production with AWS Certificate Manager

## 🚨 Troubleshooting

### Common Issues

**Container Won't Start**:
- Check CloudWatch logs in ECS
- Verify image exists in ECR
- Check task definition configuration

**Can't Access Application**:
- Verify security group rules
- Check public IP assignment
- Ensure load balancer health checks pass

**API Returns Errors**:
- Check container logs in ECS
- Verify API endpoint configuration
- Test locally with Docker Compose

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with Docker Compose
5. Submit a pull request
   
---

**Happy Calculating! 🧮**
