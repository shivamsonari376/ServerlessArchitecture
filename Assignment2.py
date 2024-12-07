import boto3
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    # Define the S3 bucket name
    bucket_name = 'serverless-arch-shivam'  # Replace with your bucket name
    
    # Initialize the S3 client
    s3_client = boto3.client('s3')
    
    # Get the current date and time
    now = datetime.now(timezone.utc)
    # Define the threshold date (30 days ago)
    threshold_date = now - timedelta(days=30)
    
    # List all objects in the S3 bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    
    # Check if the bucket has objects
    if 'Contents' in response:
        for obj in response['Contents']:
            # Get the object's last modified date
            last_modified_date = obj['LastModified']
            
            # Check if the object is older than the threshold date
            if last_modified_date < threshold_date:
                # Delete the object
                s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
                print(f"Deleted {obj['Key']} (Last Modified: {last_modified_date})")
            else:
                print(f"Kept {obj['Key']} (Last Modified: {last_modified_date})")
    else:
        print("No objects found in the bucket.")
    
    return {
        'statusCode': 200,
        'body': 'S3 bucket cleanup completed successfully!'
    }
