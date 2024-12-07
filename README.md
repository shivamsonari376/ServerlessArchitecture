# ServerlessArchitecture
Assignment 1: Automated Instance Management Using AWS Lambda and Boto3
              You're tasked to automate the stopping and starting of EC2 instances based on tags. 
          Solution:
             Created 2 instance one with Key = Action, Value = Auto-Stop-Shivam and the other one with 
                                         Key = Action, Value = Auto-Start-shivam
            and then created a lambda function which will find the instance with the help of tags and power off the instnce with             tag auto-stop and power on the instance with tag auto-start.




Assignment 2: Automated S3 Bucket Cleanup Using AWS Lambda and Boto3
       Objective: To gain experience with AWS Lambda and Boto3 by creating a Lambda function that will automatically clean up old files in an S3 bucket.
       Task: Automate the deletion of files older than 30 days in a specific S3 bucket.
