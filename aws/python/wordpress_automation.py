import boto3
# WordPress project:
# Create two security groups:
	# 1: myWebDMZ security group: INBOUND open ssh, http and https, Outbound: everything allowed
	# 2: RDSsecuritygroup: inbound: allow mysql port 3306 from Source MyWebDMZsecuritygroup.
    # 3: Create the RDS database and add it to the necessary security group.

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

# create the RDS database.

client = boto3.client('rds')

rds_database = client.create_db_instance(
    DBName='mywordpressdb',
    DBInstanceIdentifier='mywordpressadinstance',
    AllocatedStorage=5,
    DBInstanceClass='db.t2.micro',
    Engine='MySQL',
    MasterUsername='wordpressuser',
    MasterUserPassword='wordpressuserpassword',
    #DBSecurityGroups=[
    #    'string',
    #],
    VpcSecurityGroupIds=[
        sg2[u'GroupId'],
    ],
    AvailabilityZone='us-east-1a',

    DBSubnetGroupName='default',
    #PreferredMaintenanceWindow='string',
    #DBParameterGroupName='string',
    BackupRetentionPeriod=7,
    #PreferredBackupWindow='string',
    Port=3306,
    MultiAZ=False,
    EngineVersion='5.6.19a',
    AutoMinorVersionUpgrade=True|False,
    LicenseModel='general-public-license',
    #Iops=123,
    #OptionGroupName='string',
    #CharacterSetName='string',
    PubliclyAccessible=False,
    Tags=[
        {
            'Key': 'name',
            'Value': 'test_db'
        },
    ],
    #DBClusterIdentifier='string',
    StorageType='gp2',
    #TdeCredentialArn='string',
    #TdeCredentialPassword='string',
    StorageEncrypted=False,
    #KmsKeyId='string',
    #CopyTagsToSnapshot=False,
    #MonitoringInterval=60,
    #MonitoringRoleArn='string'
)