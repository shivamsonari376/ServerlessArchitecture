import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Details
    source_volume_id = 'vol-077369be204556a60'  # Your volume ID
    availability_zone = 'us-east-1a'  # Replace with your correct availability zone
    instance_type = 't2.micro'  # Instance type
    ami_id = 'ami-00f25bac1071677d3'  # Your AMI ID
    subnet_id = 'subnet-01874c4512136bd62'  # Your Subnet ID
    
    try:
        print("Fetching snapshots for volume:", source_volume_id)
        
        # Step 1: Fetch the most recent snapshot of the volume
        snapshots = ec2.describe_snapshots(
            Filters=[{'Name': 'volume-id', 'Values': [source_volume_id]}],
            OwnerIds=['self']
        )
        print(f"Found snapshots: {snapshots['Snapshots']}")
        
        if not snapshots['Snapshots']:
            raise Exception("No snapshots found for the given volume ID.")
        
        # Sort snapshots by creation date (most recent first)
        sorted_snapshots = sorted(snapshots['Snapshots'], key=lambda x: x['StartTime'], reverse=True)
        latest_snapshot_id = sorted_snapshots[0]['SnapshotId']
        print(f"Latest snapshot ID: {latest_snapshot_id}")
        
        # Step 2: Create a new volume from the snapshot
        print("Creating volume from snapshot:", latest_snapshot_id)
        new_volume = ec2.create_volume(
            SnapshotId=latest_snapshot_id,
            AvailabilityZone=availability_zone
        )
        new_volume_id = new_volume['VolumeId']
        print(f"Created new volume ID: {new_volume_id}")
        
        # Wait until the volume becomes available
        print("Waiting for volume to become available...")
        ec2.get_waiter('volume_available').wait(VolumeIds=[new_volume_id])
        print("Volume is now available.")
        
        # Step 3: Launch a new EC2 instance using the new volume
        print("Launching EC2 instance...")
        instance = ec2.run_instances(
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            SubnetId=subnet_id,  # Specify the Subnet ID
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/xvda',  # Root device name
                    'Ebs': {
                        'VolumeSize': new_volume['Size'],
                        'DeleteOnTermination': True,
                        'VolumeType': 'gp2',
                        'SnapshotId': latest_snapshot_id
                    }
                }
            ]
        )
        
        instance_id = instance['Instances'][0]['InstanceId']
        print(f"Launched new instance ID: {instance_id}")
        
        return {
            'statusCode': 200,
            'body': f"New EC2 instance {instance_id} created successfully."
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
