import psycopg2
import pandas as pd
import boto3
from io import StringIO
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

pg_host = os.getenv("HOST")
pg_database = os.getenv("DATABASE")
pg_user = os.getenv("USER")
pg_password = os.getenv("PASSWORD")
pg_port = os.getenv("PORT")

# --- PostgreSQL connection config ---
PG_CONFIG = {
    "host": pg_host,
    "database": pg_database,
    "user": pg_user,
    "password": pg_password,
    "port": pg_port
}

# --- S3 details ---
S3_BUCKET = 'prod-collection-daily-data'

# --- SQL query ---
QUERY_EP = '''
SELECT *
FROM warehouse."transaction"
WHERE DATE("createdDate") = (CURRENT_DATE - 1) AND "operatorID" = 100007;
'''
QUERY_JC = '''
SELECT *
FROM warehouse."transaction"
WHERE DATE("createdDate") = (CURRENT_DATE - 1) AND "operatorID" = 100008;
'''
QUERY_PAYMENTLOGS = '''
SELECT * FROM warehouse."paymentlogs"  WHERE "merchantID" = 1000175  AND DATE("chargedOn") = (CURRENT_DATE - 1);
'''
def get_yesterday_date():
    """Get yesterday's date in YYYY-MM-DD format"""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y%m%d')

def main(query,name):
    # Get yesterday's date for folder name
    folder_name = get_yesterday_date()
    filename = f"{name}-{folder_name}.csv"
    s3_key = f"{folder_name}/{filename}"
    
    print(f"Starting export for {folder_name}...")
    
    # Connect to PostgreSQL
    print("Connecting to PostgreSQL...")
    conn = psycopg2.connect(**PG_CONFIG)
    
    try:
        print("Executing query...")
        df = pd.read_sql_query(query, conn)
        print(f"Retrieved {len(df)} rows")
    finally:
        conn.close()
        print("Database connection closed")

    if df.empty:
        print("No data found for the given date. Skipping upload.")
        return

    # Convert DataFrame to CSV (in-memory)
    print("Creating CSV file...")
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    # Upload to S3 (using EC2 IAM Role)
    print("Uploading to S3...")
    s3 = boto3.client('s3')
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=s3_key,
        Body=csv_buffer.getvalue()
    )

    print(f"Query results uploaded to s3://{S3_BUCKET}/{s3_key}")

if __name__ == "__main__":
    main(QUERY_EP,"SP-All-transactions-EP")
    main(QUERY_JC,"SP-All-transactions_JC")
    main(QUERY_PAYMENTLOGS,"payment-logs-1000175")