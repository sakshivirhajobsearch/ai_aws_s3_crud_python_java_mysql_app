import os
import pymysql
import boto3
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# MySQL configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin')
DB_NAME = os.getenv('DB_NAME', 'ai_s3_curd')

# AWS S3 configuration from environment variables
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv('AWS_REGION', 'ap-south-1')  # default region
BUCKET_NAME = os.getenv('BUCKET_NAME', 'ai-aws-s3')

if not AWS_ACCESS_KEY or not AWS_SECRET_KEY:
    raise ValueError("AWS credentials not found in environment variables.")

# Connect to MySQL
def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# Fetch objects from S3 and insert into MySQL
def fetch_s3_objects():
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )

    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    except Exception as e:
        print(f"Error fetching S3 objects: {e}")
        return

    if 'Contents' not in response:
        print("No objects found in bucket.")
        return

    with get_connection() as conn:
        with conn.cursor() as cur:
            for obj in response['Contents']:
                object_key = obj['Key']
                size = obj['Size']
                metadata = ''
                ai_result = 'Pending'

                # Skip duplicates
                cur.execute("SELECT object_key FROM s3_objects WHERE object_key=%s", (object_key,))
                if cur.fetchone():
                    print(f"Skipped duplicate: {object_key}")
                    continue

                # Insert into MySQL
                cur.execute(
                    """
                    INSERT INTO s3_objects (object_key, bucket_name, metadata, size, ai_result)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (object_key, BUCKET_NAME, metadata, size, ai_result)
                )
                print(f"Inserted: {object_key}")

            conn.commit()

if __name__ == "__main__":
    fetch_s3_objects()
    print("S3 objects fetched and saved to MySQL successfully.")
