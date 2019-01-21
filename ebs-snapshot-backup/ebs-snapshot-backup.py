import boto3
import datetime

def notify(topic,ilist,slist,session):
  sub = "Backup Lambda executed"
  if not slist:
     msg = "No snapshots identified to remove"
  else:
     msg = """
     Instances identified: {ilist!r}
     Snapshots taken: {slist!r}
     For details, please check cloudwatch logs
     """
  snsc = session.client('sns')
  try:
     snsc.publish(TopicArn=topic,Subject=sub,Message=msg)
  except Exception as error:
     print ("Can't publish to topic " + topic + " ERROR: " + str(error))
     exit()
  print ("Published to topic" + topic)

def lambda_handler(event,context):
  if hasattr(context, 'aws_request_id'):
    print ("Running on AWS Lambda with id " + context.aws_request_id )
    session = boto3.Session()

# Script will look for these tags on the instance. It will trigger backup for all instances which have
# tags "BENVIRONMENT":"ENV1" and "BROLE":"ROLE1", or, "BENVIRONMENT":"ENV2" and "BROLE":"ROLE1"
  btags = ["ENV1","ENV2"]  
  brole = ["ROLE1"]

  sretention = 90   # Days to retain the snapshots for
  slist = []
  ilist = []
  regions = ['REGION_1','REGION_2','REGION_3'] ## Replace/add/remove regions where the instances are for backup

  for rg in regions:
     ec2c = session.client('ec2',region_name=rg )
     print ("Searching for " + str(btags) + " " + str(brole) + " instance in " + rg )
     stamp = datetime.datetime.now().strftime('%Y-%m-%d')
     delaft = str((datetime.date.today() + datetime.timedelta(days=sretention)))
     try:
       reservations = ec2c.describe_instances(Filters=[{'Name':'instance-state-name','Values':['running']}, \
       {'Name':'tag:BENVIRONMENT','Values':btags},{'Name':'tag:BROLE','Values':brole}]).get('Reservations')
     except Exception as error:
       print ("Can't get the instance list. ERROR: " + str(error))
       exit()

     if not reservations:
      print ("Can't find any!")
     else:
      print ("Found some instances! Details to follow.")

     for r in reservations:
       for i in r['Instances']:
          ilist.append(i['InstanceId'])
          for d in i['Tags']:
             if d['Key'] == 'BENVIRONMENT':
                benv = d['Value']
             if d['Key'] == 'Name':
                bname = d['Value']
             if d['Key'] == 'BROLE':
                b_role = d['Value']

          print ("Instance " + i['InstanceId'] + " : " + bname + " has " + str(len(i['BlockDeviceMappings'])) + \
          " volumes attached, will take snapshots of each")
          for v in (i['BlockDeviceMappings']):
              try:
                 snap = ec2c.create_snapshot(VolumeId=v['Ebs']['VolumeId'],Description='Auto Created by Lambda',  \
                 TagSpecifications=[{'ResourceType': 'snapshot','Tags':[{'Key': 'Name','Value': bname},  \
                 {'Key': 'Instance_Id','Value': i['InstanceId']},{'Key': 'Volume_Id','Value':v['Ebs']['VolumeId']}, \
                 {'Key':'DeleteOn','Value': delaft},{'Key':'CreatedBy','Value':'AUTO-Lambda'}, \
                 {'Key':'BENVIRONMENT','Value': benv},{'Key':'BROLE','Value': b_role}]}])
              except Exception as error:
                 print ("Could not take snapshot for " + v['Ebs']['VolumeId'] + " ERROR: " + str(error))
                 continue
              print ("Snapshot " + snap['SnapshotId'] + " taken for " + v['Ebs']['VolumeId'])
              slist.append(snap['SnapshotId'])
  
  notify(event["topic"],ilist,slist,session)
  print("Execution complete")
