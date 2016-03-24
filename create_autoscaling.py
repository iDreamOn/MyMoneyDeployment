import boto3
import datetime

client = boto3.client('autoscaling')

t = datetime.datetime.now()
e = t.strftime('%m_%d_%Y_%H_%M_%S')
name1 = 'TESTLaunchConf_'+ e
name2 = 'TESTAutoScaling_' + e

# Create launch configuration
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

# create auto scaling group
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

# put scaling policy to decrease
policy1 = client.put_scaling_policy(
    AutoScalingGroupName=name2,
    PolicyName='Decrease Group Size',
    PolicyType='SimpleScaling',
    AdjustmentType='ChangeInCapacity',
    ScalingAdjustment=-1,
)

# put scaling policy to increase
policy2 = client.put_scaling_policy(
    AutoScalingGroupName=name2,
    PolicyName='Increase Group Size',
    PolicyType='SimpleScaling',
    AdjustmentType='ChangeInCapacity',
    ScalingAdjustment=1,
)
# Create a SNS topic
client = boto3.client('sns')
mytopic = client.create_topic(
    Name='AlertMeonEmailPLZ_'+e
)
mysubscription = client.subscribe(
    TopicArn=mytopic[u'TopicArn'],
    Protocol='email',
    Endpoint='sns@uzuro.33mail.com'
)


# put alarm for policy
client = boto3.client('cloudwatch')
# alarm for decrease policy
response = client.put_metric_alarm(
    AlarmName='CPUbelow80',
    AlarmDescription='alert if CPU utilization is below 80%',
    ActionsEnabled=True,
    AlarmActions=[
        policy1[u'PolicyARN'], mytopic[u'TopicArn'],
    ],
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Statistic='Average',
    Dimensions=[
        {
            'Name': 'AutoScalingGroupName',
            'Value': name2
        },
    ],
    Period=300,
    EvaluationPeriods=1,
    Threshold=80,
    ComparisonOperator='LessThanOrEqualToThreshold'
)

# alarm for increase policy
response = client.put_metric_alarm(
    AlarmName='CPUover80',
    AlarmDescription='alert if CPU utilization is above 80%',
    ActionsEnabled=True,
    AlarmActions=[
        policy2[u'PolicyARN'], mytopic[u'TopicArn'],
    ],
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Statistic='Average',
    Dimensions=[
        {
            'Name': 'AutoScalingGroupName',
            'Value': name2
        },
    ],
    Period=300,
    EvaluationPeriods=1,
    Threshold=80,
    ComparisonOperator='GreaterThanOrEqualToThreshold'
)

