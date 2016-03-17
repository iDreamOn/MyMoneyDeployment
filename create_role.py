import boto3
import datetime

'''client = boto3.client('iam')
# Create the S3 access role
s3role = client.create_role(
    RoleName='S3_Access_Role_Wordpress',
    AssumeRolePolicyDocument= '{"Version": "2012-10-17","Statement": {"Effect": "Allow","Principal": {"Service": "ec2.amazonaws.com"},"Action": "sts:AssumeRole"}}'
)
# attach a policy (AWSs3FullAcess) to the role.
policy = client.attach_role_policy(
    RoleName=s3role[u'Role'][u'RoleName'],
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'
)

# get a security group
# sg-2fcc1f57
'''
# Create a keypair
ec2 = boto3.resource('ec2')


t = datetime.datetime.now()
e = t.strftime('%m/%d/%Y/%H/%M/%S')
name = 'key_'+ e
key_pair = ec2.create_key_pair(
    DryRun= False,
    KeyName= name
)

print key_pair
# create the EC2 instance with the proper information.
ec2 = boto3.resource('ec2')

instance = ec2.create_instances(
    DryRun=False,
    ImageId='ami-60b6c60a',
    MinCount=1,
    MaxCount=1,
    KeyName=name,
    SecurityGroupIds=[
        'sg-2fcc1f57',
    ],
    #UserData='string',
    InstanceType='t2.micro',

)