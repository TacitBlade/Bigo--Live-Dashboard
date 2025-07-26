#!/bin/bash

# Bigo Live Dashboard AWS Deployment Script
# This script deploys the dashboard to AWS Elastic Beanstalk

set -e  # Exit on any error

echo "🚀 Starting Bigo Live Dashboard Deployment..."

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first."
    echo "Visit: https://aws.amazon.com/cli/"
    exit 1
fi

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    echo "📦 Installing AWS Elastic Beanstalk CLI..."
    pip install awsebcli
fi

# Configuration
APP_NAME="bigo-live-dashboard"
ENV_NAME="bigo-dashboard-prod"
REGION="us-east-1"

echo "📋 Configuration:"
echo "   App Name: $APP_NAME"
echo "   Environment: $ENV_NAME"
echo "   Region: $REGION"

# Check if .elasticbeanstalk directory exists
if [ ! -d ".elasticbeanstalk" ]; then
    echo "🔧 Initializing Elastic Beanstalk application..."
    eb init $APP_NAME --region $REGION --platform python-3.9
else
    echo "✅ Elastic Beanstalk already initialized"
fi

# Create .ebextensions directory if it doesn't exist
if [ ! -d ".ebextensions" ]; then
    echo "📁 Creating .ebextensions directory..."
    mkdir .ebextensions
fi

# Create Streamlit configuration for EB
cat > .ebextensions/streamlit.config << EOF
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: application.py
  aws:elasticbeanstalk:application:environment:
    STREAMLIT_SERVER_PORT: 8501
    STREAMLIT_SERVER_ADDRESS: 0.0.0.0
    STREAMLIT_BROWSER_GATHER_USAGE_STATS: false
    ENVIRONMENT: production

files:
  "/opt/elasticbeanstalk/tasks/taillogs.d/streamlit.conf":
    mode: "000644"
    owner: root
    group: root
    content: |
      /tmp/streamlit.log

commands:
  01_install_streamlit:
    command: "pip install streamlit"
  02_start_streamlit:
    command: "streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > /tmp/streamlit.log 2>&1 &"
EOF

# Create application.py for EB (required)
if [ ! -f "application.py" ]; then
    echo "📄 Creating application.py for Elastic Beanstalk..."
    cat > application.py << 'EOF'
import subprocess
import sys
import os

# Set environment variables
os.environ['STREAMLIT_SERVER_PORT'] = '8501'
os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

# Start Streamlit
if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"])
EOF
fi

# Check if environment exists
if eb list | grep -q $ENV_NAME; then
    echo "🔄 Environment $ENV_NAME exists. Deploying updates..."
    eb deploy $ENV_NAME
else
    echo "🆕 Creating new environment $ENV_NAME..."
    eb create $ENV_NAME --instance-type t3.micro --region $REGION
fi

echo "✅ Deployment completed!"
echo "🌐 Your dashboard should be available at the EB environment URL"
echo "📊 Run 'eb open' to view your deployed application"

# Optional: Open the application
read -p "🔗 Would you like to open the application now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    eb open
fi

echo "🎉 Deployment script finished!"
