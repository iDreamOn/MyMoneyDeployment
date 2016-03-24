import boto3
import datetime

client = boto3.client('autoscaling')

t = datetime.datetime.now()
e = t.strftime('%m_%d_%Y_%H_%M_%S')
name1 = 'TESTLaunchConf_'+ e
name2 = 'TESTAutoScaling_' + e
'''
response = client.create_launch_configuration(
    LaunchConfigurationName=name1,
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
                'VolumeSize': 8,
                'VolumeType': 'gp2',
                'DeleteOnTermination': True,
            },
        },
    ],
    InstanceMonitoring={
        'Enabled': False
    },
    IamInstanceProfile='S3-Admin-Access',
    EbsOptimized=False
)


response = client.create_auto_scaling_group(
    AutoScalingGroupName=name2,
    LaunchConfigurationName=name1,
    MinSize=1,
    MaxSize=3,
    DesiredCapacity=1,
    DefaultCooldown=300,
    #AvailabilityZones=[
    #    'us-east-1c',
    #],
    LoadBalancerNames=[
        'MyTestLB12',
    ],
    HealthCheckType='ELB',
    HealthCheckGracePeriod=300,
    VPCZoneIdentifier='subnet-3d75144a,subnet-4265ca69,subnet-3839be61',
    TerminationPolicies=[
        'Default',
    ],
    NewInstancesProtectedFromScaleIn=False,
    Tags=[
        {
            'ResourceId': name2,
            'ResourceType': 'auto-scaling-group',
            'Key': 'ASGname',
            'Value': 'AUTOSCALINGVALUETEST',
            'PropagateAtLaunch': True
        },
    ]
)
'''
name2='TESTAutoScaling_03_24_2016_16_33_27'

#put scaling policy to decrease
response = client.put_scaling_policy(
    AutoScalingGroupName=name2,
    PolicyName='Decrease Group Size',
    PolicyType='SimpleScaling',
    AdjustmentType='ChangeInCapacity',
    ScalingAdjustment=-1,
)
#put alarm for policy


#put scaling policy to increase
response = client.put_scaling_policy(
    AutoScalingGroupName=name2,
    PolicyName='Increase Group Size',
    PolicyType='SimpleScaling',
    AdjustmentType='ChangeInCapacity',
    ScalingAdjustment=1,
)