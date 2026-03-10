# Driver Pulse Deployment Instructions

## Overview

This guide provides step-by-step instructions for deploying Driver Pulse in various environments, from local development to production cloud deployment.

## Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: Minimum 2GB free space
- **Operating System**: Windows 10+, macOS 10.14+, or Linux

### Required Software
- Python 3.8+ with pip
- Git (for cloning repository)
- Docker (optional, for containerized deployment)
- Docker Compose (optional, for multi-container setup)

## Local Development Deployment

### Option 1: Direct Python Installation

1. **Clone the Repository**
```bash
git clone <repository-url>
cd driver-pulse
```

2. **Create Virtual Environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Generate Sample Data**
```bash
python main.py --generate-sample-data
```

5. **Run the Dashboard**
```bash
streamlit run dashboard/app.py
```

6. **Access the Application**
Open your browser and navigate to: http://localhost:8501

### Option 2: Docker Deployment

1. **Clone the Repository**
```bash
git clone <repository-url>
cd driver-pulse
```

2. **Build and Run with Docker Compose**
```bash
docker-compose up --build
```

3. **Access the Application**
Open your browser and navigate to: http://localhost:8501

4. **Stop the Application**
```bash
docker-compose down
```

## Cloud Deployment

### Streamlit Community Cloud (Recommended)

#### Prerequisites
- GitHub account
- Streamlit Community Cloud account

#### Steps

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit - Driver Pulse"
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Deploy to Streamlit Cloud**
- Go to [share.streamlit.io](https://share.streamlit.io)
- Click "New app"
- Connect your GitHub repository
- Select the repository and branch
- Set the main file path to: `dashboard/app.py`
- Click "Deploy"

3. **Configure Environment Variables** (if needed)
- In your Streamlit app settings, add any required environment variables
- Common variables:
  - `PYTHONPATH`: `/app`
  - `STREAMLIT_SERVER_PORT`: `8501`

4. **Data Setup**
- The app will automatically generate sample data on first run
- For production, you'll need to set up automated data processing

#### Automated Data Processing

Option 1: **GitHub Actions**
```yaml
# .github/workflows/process-data.yml
name: Process Driver Data

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  process:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Process data
        run: python main.py
      - name: Commit outputs
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add outputs/
          git commit -m "Update processed data" || exit 0
          git push
```

Option 2: **External Cron Job**
Set up a cron job on a server to run the data processing:
```bash
# Every hour
0 * * * * cd /path/to/driver-pulse && /path/to/venv/bin/python main.py
```

### AWS Deployment

#### Using EC2

1. **Launch EC2 Instance**
- Choose Ubuntu 20.04 LTS or Amazon Linux 2
- Select t3.medium instance type or larger
- Configure security group to allow port 8501

2. **Connect to Instance**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install Dependencies**
```bash
sudo apt update
sudo apt install -y python3 python3-pip git
git clone <repository-url>
cd driver-pulse
pip3 install -r requirements.txt
```

4. **Run Application**
```bash
python3 main.py --generate-sample-data
streamlit run dashboard/app.py --server.address=0.0.0.0
```

5. **Access Application**
Navigate to: http://your-ec2-ip:8501

#### Using ECS (Elastic Container Service)

1. **Create Repository**
```bash
aws ecr create-repository --repository-name driver-pulse
```

2. **Build and Push Image**
```bash
# Get login token
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.us-west-2.amazonaws.com

# Build image
docker build -t driver-pulse .

# Tag image
docker tag driver-pulse:latest <aws-account-id>.dkr.ecr.us-west-2.amazonaws.com/driver-pulse:latest

# Push image
docker push <aws-account-id>.dkr.ecr.us-west-2.amazonaws.com/driver-pulse:latest
```

3. **Create Task Definition**
```json
{
  "family": "driver-pulse",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "driver-pulse",
      "image": "<aws-account-id>.dkr.ecr.us-west-2.amazonaws.com/driver-pulse:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "STREAMLIT_SERVER_ADDRESS",
          "value": "0.0.0.0"
        }
      ]
    }
  ]
}
```

4. **Create Service**
- Use the AWS Console or CLI to create a service
- Configure load balancer for external access
- Set up auto-scaling if needed

### Google Cloud Platform Deployment

#### Using Cloud Run

1. **Enable APIs**
```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

2. **Build and Deploy**
```bash
# Build image
gcloud builds submit --tag gcr.io/PROJECT-ID/driver-pulse

# Deploy to Cloud Run
gcloud run deploy driver-pulse \
  --image gcr.io/PROJECT-ID/driver-pulse \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8501
```

3. **Access Application**
Cloud Run will provide a URL for your deployed application.

### Azure Deployment

#### Using Container Instances

1. **Create Resource Group**
```bash
az group create --name driver-pulse-rg --location eastus
```

2. **Build and Push Image**
```bash
# Build image
docker build -t driver-pulse .

# Tag for Azure
docker tag driver-pulse:latest yourregistry.azurecr.io/driver-pulse:latest

# Push to Azure Container Registry
docker push yourregistry.azurecr.io/driver-pulse:latest
```

3. **Deploy Container**
```bash
az container create \
  --resource-group driver-pulse-rg \
  --name driver-pulse-app \
  --image yourregistry.azurecr.io/driver-pulse:latest \
  --dns-name-label driver-pulse-unique \
  --ports 8501 \
  --environment-variables 'STREAMLIT_SERVER_ADDRESS=0.0.0.0'
```

## Production Considerations

### Security

1. **Environment Variables**
- Store sensitive data in environment variables
- Use secret management services (AWS Secrets Manager, Azure Key Vault)
- Never commit secrets to version control

2. **Network Security**
- Use HTTPS in production
- Configure firewalls and security groups
- Implement rate limiting
- Use CDN for static assets

3. **Authentication**
- Implement user authentication for production
- Use OAuth 2.0 or similar standards
- Consider role-based access control

### Performance

1. **Database Optimization**
- Replace CSV files with proper database
- Implement indexing for frequently queried data
- Use connection pooling
- Consider read replicas for scaling

2. **Caching**
- Implement Redis or similar for caching
- Cache frequently accessed data
- Use CDN for static assets
- Implement browser caching

3. **Load Balancing**
- Use load balancers for high availability
- Implement health checks
- Configure auto-scaling
- Monitor performance metrics

### Monitoring

1. **Application Monitoring**
- Implement APM (Application Performance Monitoring)
- Track key metrics: response time, error rate, throughput
- Set up alerts for critical issues
- Monitor resource usage

2. **Logging**
- Implement structured logging
- Use centralized logging (ELK stack, Splunk)
- Log security events
- Regular log analysis

3. **Health Checks**
- Implement health check endpoints
- Monitor system dependencies
- Set up uptime monitoring
- Create incident response procedures

### Backup and Recovery

1. **Data Backup**
- Regular database backups
- Automated backup schedules
- Off-site backup storage
- Backup encryption

2. **Disaster Recovery**
- Document recovery procedures
- Test recovery scenarios
- Maintain recovery time objectives (RTO)
- Maintain recovery point objectives (RPO)

## Troubleshooting

### Common Issues

1. **Port Already in Use**
```bash
# Find process using port 8501
lsof -i :8501
# Kill the process
kill -9 <PID>
# Or use different port
streamlit run dashboard/app.py --server.port 8502
```

2. **Memory Issues**
```bash
# Reduce data chunk size in config
# Use data sampling for large datasets
# Increase system memory or use cloud deployment
```

3. **Import Errors**
```bash
# Check Python version (3.8+)
# Verify all dependencies installed
# Check PYTHONPATH environment variable
```

4. **Docker Issues**
```bash
# Clear Docker cache
docker system prune -a
# Rebuild image
docker-compose build --no-cache
# Check container logs
docker-compose logs dashboard
```

### Performance Issues

1. **Slow Dashboard Loading**
- Check data file sizes
- Optimize data processing
- Implement data pagination
- Use data sampling

2. **High Memory Usage**
- Reduce chunk size in configuration
- Enable data garbage collection
- Use more efficient data structures
- Scale up resources

3. **Slow Data Processing**
- Enable parallel processing
- Optimize algorithms
- Use vectorized operations
- Consider distributed processing

## Maintenance

### Regular Tasks

1. **Daily**
- Monitor system performance
- Check error logs
- Verify data processing completion

2. **Weekly**
- Review security logs
- Update dependencies
- Check storage usage
- Performance optimization

3. **Monthly**
- Security updates
- Backup verification
- Performance review
- Capacity planning

### Updates and Patches

1. **Application Updates**
- Test updates in staging
- Use blue-green deployment
- Monitor post-deployment
- Rollback plan ready

2. **Security Updates**
- Regular security scans
- Prompt patch application
- Vulnerability assessment
- Security audit reviews

## Support

### Getting Help

1. **Documentation**
- Check this deployment guide
- Review API documentation
- Consult troubleshooting section

2. **Community Support**
- GitHub Issues for bug reports
- Community forums for questions
- Stack Overflow for technical issues

3. **Professional Support**
- Contact development team
- Enterprise support options
- Consulting services

### Contact Information

- **Technical Support**: tech-support@driverpulse.com
- **Documentation**: docs@driverpulse.com
- **Sales**: sales@driverpulse.com
- **General Info**: info@driverpulse.com

---

**Last Updated**: March 2024  
**Version**: 1.0  
**Maintained by**: Team Velocity
