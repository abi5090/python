import boto3
import time
import datetime

accountId = '<enter your aws account number here>'
ec2c = boto3.client('ec2')
stamp = datetime.datetime.now().strftime('%Y-%m-%d')
delaft = (datetime.date.today() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')

reservations = ec2c.describe_instances(Filters=[{'Name':'tag-key','Values':['Backup']}]).get('Reservations')

# count and list the instances identified for backup #

for r in reservations:
  for i in r['Instances']:
    print ("Backup Tag found on Instance: " + i['InstanceId'])
    for d in i['Tags']:
      if d['Key'] == 'Name':
        name = "AUTO-" + d['Value'] + "-" + stamp
        break
      else:
        name = "AUTO-" + stamp
    print ("Initiate AMI creation: " + name)
    amiId = ec2c.create_image(InstanceId=i['InstanceId'], Name=name, Description="AUTO created on " + stamp, NoReboot=True)
    print (amiId)
    time.sleep(5)
    print ("Update Tags on AMI, Snapshot")
    resources = []
    resources.append(amiId['ImageId'])
    ami = ec2c.describe_images(Owners=[accountId],ImageIds=[amiId['ImageId']])
    for bd in ami['Images'][0].get('BlockDeviceMappings'):
       resources.append(bd['Ebs'].get('SnapshotId'))
    amiTag = ec2c.create_tags(Resources=resources,Tags=[{'Key':'Name','Value': name},{'Key': 'Delete After','Value': delaft}])

print ("Completed")
