import boto3
import time
import datetime

accountId = 'AWS_ACCOUNT_NUMBER'
ec2c = boto3.client('ec2')

amis = ec2c.describe_images(Owners=[accountId])
delt = (datetime.date.today().strftime('%Y-%m-%d'))

delamis = []
delsnaps = []

# count and list the instances identified for backup #
for a in amis['Images']:
   if a['Name'].startswith('AUTO-'):
      for d in a['Tags']:
         if d['Key'] == "Delete After":
           delaft = d['Value']
           break
         else:
           delaft = ''
   else:
      continue
       
   if delaft and ( delaft < delt ):
      print ("AMI can be removed: ",a['ImageId'])
      delamis.append(a['ImageId'])
      for bd in a['BlockDeviceMappings']:
         delsnaps.append(bd.get('Ebs')['SnapshotId'])

   else:
      print ("Unable to decide about AMI: " + a['ImageId'])
      print ("Please check the Delete After tag on this AMI")
      continue

print ("Removing AMIs: " + str(delamis))
print ("Removing Snapshots: " + str(delsnaps))

# remove amis
for ami in delamis:
   resp = ec2c.deregister_image(ImageId=ami,DryRun=False)
   print (resp)

time.sleep(5)
# remove snapshots
for snap in delsnaps:
   resp = ec2c.delete_snapshot(SnapshotId=snap,DryRun=False)
   print (resp)

print ("Completed")
