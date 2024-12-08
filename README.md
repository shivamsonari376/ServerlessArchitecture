# ServerlessArchitecture
Assignment 1: Automated Instance Management Using AWS Lambda and Boto3
              You're tasked to automate the stopping and starting of EC2 instances based on tags. 
          Solution:
             Created 2 instance one with Key = Action, Value = Auto-Stop-Shivam and the other one with 
                                         Key = Action, Value = Auto-Start-shivam
            and then created a lambda function which will find the instance with the help of tags and power off the instnce with tag auto-stop and power on the instance with tag auto-start.




Assignment 2: Automated S3 Bucket Cleanup Using AWS Lambda and Boto3
       Objective: To gain experience with AWS Lambda and Boto3 by creating a Lambda function that will automatically clean up old files in an S3 bucket.
       Task: Automate the deletion of files older than 30 days in a specific S3 bucket.
       Solution: Created an s3 bucket with my name uploaded files and deleted the older files.


Assignment 6: Monitor and Alert High AWS Billing Using AWS Lambda, Boto3, and SNS
         Objective: Create an automated alerting mechanism for when your AWS billing exceeds a certain threshold.
         Task: Set up a Lambda function to check your AWS billing amount daily, and if it exceeds a specified threshold, send an alert via SNS.
         Solution: Created a threshold of 1usd to send emails. Created a lambda function and received a test email at my registered email id.


Assignment17: Objective: Automate the process of creating a new EC2 instance from the latest snapshot using a Lambda function.
        Solution: Create a AMI from the source EC2 instance and capture the voulume id of source EC2 instance and the AMI ID and VPC details and create a new lambda function with these details.
