"""
AWS configuration and deployment settings.
Contains AWS-specific configuration for deploying the Bigo Live Dashboard.
"""

import os
from typing import Dict, Optional

# AWS General Settings
AWS_REGION = "us-east-1"
AWS_PROFILE = "default"

# Elastic Beanstalk Settings
BEANSTALK_CONFIG = {
    "application_name": "bigo-live-dashboard",
    "environment_name": "bigo-dashboard-prod",
    "platform": "python-3.9",
    "instance_type": "t3.micro",
    "min_instances": 1,
    "max_instances": 3,
}

# S3 Settings
S3_CONFIG = {
    "bucket_name": "bigo-dashboard-assets",
    "region": AWS_REGION,
    "public_read": False,
}

# RDS Settings (if using database)
RDS_CONFIG = {
    "engine": "mysql",
    "instance_class": "db.t3.micro",
    "allocated_storage": 20,
    "database_name": "bigo_dashboard",
    "backup_retention": 7,
}

# CloudWatch Settings
CLOUDWATCH_CONFIG = {
    "log_group": "/aws/elasticbeanstalk/bigo-dashboard",
    "retention_days": 14,
}

# Environment Variables for AWS
AWS_ENV_VARS = {
    "STREAMLIT_SERVER_PORT": "8501",
    "STREAMLIT_SERVER_ADDRESS": "0.0.0.0",
    "STREAMLIT_BROWSER_GATHER_USAGE_STATS": "false",
    "ENVIRONMENT": "production",
}

def get_aws_region() -> str:
    """Get AWS region from environment or default."""
    return os.getenv("AWS_REGION", AWS_REGION)

def get_aws_profile() -> str:
    """Get AWS profile from environment or default."""
    return os.getenv("AWS_PROFILE", AWS_PROFILE)

def get_beanstalk_config() -> Dict[str, str]:
    """Get Elastic Beanstalk configuration."""
    config = BEANSTALK_CONFIG.copy()
    
    # Override with environment variables if available
    config["application_name"] = os.getenv("EB_APP_NAME", config["application_name"])
    config["environment_name"] = os.getenv("EB_ENV_NAME", config["environment_name"])
    
    return config

def get_s3_bucket_name() -> str:
    """Get S3 bucket name."""
    return os.getenv("S3_BUCKET", S3_CONFIG["bucket_name"])

def get_database_url() -> Optional[str]:
    """Get database URL if configured."""
    return os.getenv("DATABASE_URL")

def is_aws_configured() -> bool:
    """Check if AWS credentials are configured."""
    return bool(
        os.getenv("AWS_ACCESS_KEY_ID") or 
        os.path.exists(os.path.expanduser("~/.aws/credentials"))
    )

def get_deployment_command() -> str:
    """Get the deployment command for AWS."""
    return """
    # Deploy to AWS Elastic Beanstalk
    pip install awsebcli
    eb init {app_name} --region {region}
    eb create {env_name}
    eb deploy
    """.format(
        app_name=BEANSTALK_CONFIG["application_name"],
        region=get_aws_region(),
        env_name=BEANSTALK_CONFIG["environment_name"]
    )

# AWS CLI Configuration
def generate_aws_config():
    """Generate AWS configuration for deployment."""
    return {
        "AWSEBDockerrunVersion": 2,
        "containerDefinitions": [
            {
                "name": "bigo-dashboard",
                "image": "python:3.9-slim",
                "essential": True,
                "memory": 512,
                "portMappings": [
                    {
                        "hostPort": 80,
                        "containerPort": 8501
                    }
                ],
                "environment": [
                    {"name": k, "value": v} for k, v in AWS_ENV_VARS.items()
                ]
            }
        ]
    }
