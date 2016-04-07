import boto3
import datetime



ec2 = boto3.resource('ec2')

# Create a keypair
t = datetime.datetime.now()
e = t.strftime('%m/%d/%Y/%H/%M/%S')
name = 'key_'+ e
key_pair = ec2.create_key_pair(
    DryRun= False,
    KeyName= name
)

name = 'TESTING'
user_data2='''#!/bin/bash
yum install -y curl gpg gcc gcc-c++ make
gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
\curl -sSL https://get.rvm.io | bash -s stable --ruby --rails
source /home/ec2-user/.rvm/scripts/rvm
source /etc/profile.d/rvm.sh 
yum install -y epel-release
yum install -y --enablerepo=epel nodejs npm
yum install -y libcurl-devel
gem install bundler --no-rdoc --no-ri
gem install passenger --no-rdoc --no-ri
passenger-install-nginx-module --auto --auto-download --languages 'ruby'
/opt/nginx/sbin/nginx'''

###########################################3
#print key_pair
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
    UserData=user_data2,
    InstanceType='t2.micro',
)
