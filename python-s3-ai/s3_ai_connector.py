# s3_ai_connector.py

import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, ClientError

# Load environment variables from .env file
load_dotenv()

# Fetch AWS credentials from environment
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")  # Default region if not provided

# Validate credentials
if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
    raise ValueError("AWS credentials not found in environment variables. "
                     "Please check your .env file or set them in your environment.")

# Initialize S3 client
try:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
except NoCredentialsError:
    raise ValueError("Failed to authenticate AWS credentials.")
except Exception as e:
    raise RuntimeError(f"Error initializing S3 client: {e}")

# Example function: list all S3 buckets
def fetch_s3_buckets():
    try:
        response = s3_client.list_buckets()
        print("S3 Buckets:")
        for bucket in response.get('Buckets', []):
            print(f" - {bucket['Name']}")
    except ClientError as e:
        print(f"Error fetching S3 buckets: {e}")

if __name__ == "__main__":
    fetch_s3_buckets()
