import boto3
#W ordPress project:
# Create two security groups:
	# 1: myWebDMZ security group: INBOUND open ssh, http and https, Outbound: everything allowed
	# 2: RDSsecuritygroup: inbound: allow mysql port 3306 from Source MyWebDMZsecuritygroup.

# Create the AMI (Amazon Machine Image)    

client = boto3.client('ec2')
# Get the default VPC's ID. We can create our own VPC later on.
default_vpc_id ='vpc-1cc89d79'

# Creating Security Group 1
sg1 = client.create_security_group(
    DryRun=False,
    GroupName='SG1a',
    Description='MyWebDMZsecuritygroup',
    VpcId=default_vpc_id
    )

# Open the inbound ports : 80, 443, 22
rule1 = client.authorize_security_group_ingress(
	DryRun=False,
    GroupId=sg1[u'GroupId'],
    IpPermissions=[ {'IpProtocol': 'TCP', 'FromPort': 80,  'ToPort': 80,  'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
				    {'IpProtocol': 'TCP', 'FromPort': 443, 'ToPort': 443, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
				    {'IpProtocol': 'TCP', 'FromPort': 22,  'ToPort': 22,  'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
				  ]
    )
# Create Security Group 2
sg2 = client.create_security_group(
    DryRun=False,
    GroupName='SG1b',
    Description='RDSsecuritygroup',
    VpcId=default_vpc_id
    )
# Open the inbound ports : 3306 to the MYWebDMZsecuritygroup sg1
rule2 = client.authorize_security_group_ingress(
	DryRun=False,
    GroupId=sg2[u'GroupId'],
    IpPermissions=[ {'IpProtocol': 'TCP', 'FromPort': 3306,  'ToPort': 3306, 'UserIdGroupPairs': [{'GroupId': sg1[u'GroupId']}]}]

)