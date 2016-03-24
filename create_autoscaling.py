import boto3

client = boto3.client('autoscaling')

response = client.create_launch_configuration(
    LaunchConfigurationName='TESTING_LaunchCF',
    ImageId='ami-71cdf01b',
    KeyName='MyEC2key',
    SecurityGroups=[
        'sg-2fcc1f57',
    ],
    #UserData='string',
    InstanceType='t2.micro',
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {
                'SnapshotId': 'string',
                'VolumeSize': 8,
                'VolumeType': 'gp2',
                'DeleteOnTermination': True,
                'Encrypted': False
            },
        },
    ],
    InstanceMonitoring={
        'Enabled': False
    },
    IamInstanceProfile='S3-Admin-Access',
    EbsOptimized=False
)
