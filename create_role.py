import boto3
client = boto3.client('iam')
# Create the S3 access role
s3role = client.create_role(
    RoleName='S3_Access_Role_test',
    AssumeRolePolicyDocument= '{"Version": "2012-10-17","Statement": {"Effect": "Allow","Principal": {"Service": "ec2.amazonaws.com"},"Action": "sts:AssumeRole"}}'
)
