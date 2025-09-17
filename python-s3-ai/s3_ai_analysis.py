import pymysql
import random
import os
from dotenv import load_dotenv

# Load environment variables from .env (optional if you want to configure DB via env)
load_dotenv()

# MySQL configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin')
DB_NAME = os.getenv('DB_NAME', 'ai_s3_curd')

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

# Mock AI analysis function
def perform_ai_analysis(object_key):
    """
    Simulate AI analysis. Replace this with real AI model inference.
    """
    labels = ['Safe', 'Adult Content', 'Violence', 'Sensitive', 'Normal']
    return random.choice(labels)

def analyze_s3_objects():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Fetch all S3 objects
                cur.execute("SELECT id, object_key FROM s3_objects")
                objects = cur.fetchall()

                if not objects:
                    print("No objects found in database.")
                    return

                for obj in objects:
                    object_id = obj['id']
                    object_key = obj['object_key']

                    # Perform mock AI analysis
                    result = perform_ai_analysis(object_key)

                    # Update the ai_result field
                    cur.execute(
                        "UPDATE s3_objects SET ai_result=%s WHERE id=%s",
                        (result, object_id)
                    )
                    print(f"Updated AI result for {object_key}: {result}")

            conn.commit()
            print("All AI analysis results updated successfully.")

    except pymysql.MySQLError as e:
        print(f"MySQL Error: {e}")

if __name__ == "__main__":
    analyze_s3_objects()
