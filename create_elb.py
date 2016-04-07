import boto3
import datetime

client = boto3.client('elb')

t = datetime.datetime.now()
e = t.strftime('%m/%d/%Y/%H/%M/%S')
name1 = 'TESTELB_'+ e

elb = client.create_load_balancer(
    LoadBalancerName='MyTestLB12',
    Listeners=[
        {
            'Protocol': 'HTTP',
            'LoadBalancerPort': 80,
            'InstanceProtocol': 'HTTP',
            'InstancePort': 80
        },
    ],
    Subnets=[
        'subnet-3839be61', 'subnet-3d75144a', 'subnet-4265ca69', 'subnet-d4d287ee'
    ],
    
    SecurityGroups=[
        'sg-2fcc1f57',
    ],
    Tags=[
        {
            'Key': 'NameOfELB',
            'Value': 'TESTING_OF_ELB_TAG'
        },
    ]
)

response = client.configure_health_check(
    LoadBalancerName='MyTestLB12',
    HealthCheck={
        'Target': 'HTTP:80/elb.html',
        'Interval': 30,
        'Timeout': 5,
        'UnhealthyThreshold': 4,
        'HealthyThreshold': 4
    }
)