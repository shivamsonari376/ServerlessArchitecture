# ServerlessArchitecture
Assignment 1: Automated Instance Management Using AWS Lambda and Boto3
              You're tasked to automate the stopping and starting of EC2 instances based on tags. 
          Solution:
             Created 2 instance one with Key = Action, Value = Auto-Stop-Shivam and the other one with 
                                         Key = Action, Value = Auto-Start-shivam
            and then created a lambda function which will find the instance with the help of tags and power off the instnce with             tag auto-stop and power on the instance with tag auto-start.
