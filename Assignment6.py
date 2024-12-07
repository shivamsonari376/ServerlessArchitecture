import boto3
from datetime import datetime, timedelta

# Initialize Boto3 clients for CloudWatch and SNS
cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')  # Use your billing region
sns = boto3.client('sns')

# Define your SNS topic ARN and billing threshold
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:975050024946:BillingAlertsTopicShivam'  # Replace with your SNS topic ARN
BILLING_THRESHOLD = 1.0  # Replace with your desired threshold in USD

def lambda_handler(event, context):
    # Get the current and previous day's timestamps for the billing metric
    now = datetime.utcnow()
    start_time = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = now.replace(hour=0, minute=0, second=0, microsecond=0)

    try:
        # Retrieve the EstimatedCharges metric from CloudWatch
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/Billing',
            MetricName='EstimatedCharges',
            Dimensions=[
                {
                    'Name': 'Currency',
                    'Value': 'USD'  # Replace 'USD' if your billing is in another currency
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=86400,  # 1 day in seconds
            Statistics=['Maximum']
        )

        # Extract the maximum billing amount
        data_points = response['Datapoints']
        if data_points:
            max_billing = data_points[-1]['Maximum']
            print(f"Current billing amount: ${max_billing}")

            # Check if the billing exceeds the threshold
            if max_billing > BILLING_THRESHOLD:
                # Send an SNS alert
                alert_message = f"ALERT: Your AWS billing has exceeded the threshold of ${BILLING_THRESHOLD}. Current amount: ${max_billing}."
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject='AWS Billing Alert',
                    Message=alert_message
                )
                print(f"SNS alert sent: {alert_message}")
            else:
                print(f"Billing is under control: ${max_billing}")
        else:
            print("No billing data found for the specified time range.")
    
    except Exception as e:
        print(f"Error retrieving billing data: {e}")
    
    return {
        'statusCode': 200,
        'body': 'Billing check completed successfully!'
    }
