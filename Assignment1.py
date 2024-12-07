import boto3

def lambda_handler(event, context):
    # Initialize EC2 client
    ec2_client = boto3.client('ec2')
    
    # Describe instances with the Auto-stop_Shivam tag
    auto_stop_instances = ec2_client.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-stop_Shivam']}
        ]
    )
    
    # Describe instances with the Auto-start_Shivam tag
    auto_start_instances = ec2_client.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-start_Shivam']}
        ]
    )
    
    # Collect instance IDs for stopping
    stop_instance_ids = [
        instance['InstanceId']
        for reservation in auto_stop_instances['Reservations']
        for instance in reservation['Instances']
        if instance['State']['Name'] != 'stopped'  # Skip already stopped instances
    ]
    
    # Collect instance IDs for starting
    start_instance_ids = [
        instance['InstanceId']
        for reservation in auto_start_instances['Reservations']
        for instance in reservation['Instances']
        if instance['State']['Name'] != 'running'  # Skip already running instances
    ]
    
    # Stop instances
    if stop_instance_ids:
        ec2_client.stop_instances(InstanceIds=stop_instance_ids)
        print(f"Stopped instances: {stop_instance_ids}")
    else:
        print("No instances to stop.")
    
    # Start instances
    if start_instance_ids:
        ec2_client.start_instances(InstanceIds=start_instance_ids)
        print(f"Started instances: {start_instance_ids}")
    else:
        print("No instances to start.")
    
    return {
        'statusCode': 200,
        'body': {
            'StoppedInstances': stop_instance_ids,
            'StartedInstances': start_instance_ids
        }
    }
