import boto3
import time
import datetime

def notify(topic,slist,session):
  sub = "Cleanup Lambda executed"
  if not slist:
     msg = "No snapshots identified to remove"
  else:
     msg = "\nSnapshots removed: {}\n\n\nFor details, please check cloudwatch logs".format(",".join(slist))
  snsc = session.client('sns')
  try:
     resp = snsc.publish(TopicArn=topic,Subject=sub,Message=msg)
  except Exception as error:
     print ("Can't publish to topic " + topic + " ERROR: " + str(error))
     exit()
  print ("Published to topic" + topic)

def lambda_handler(event,context):
  if hasattr(context, 'aws_request_id'):
    print ("Running on AWS Lambda with id " + context.aws_request_id )
    session = boto3.Session()

  ownerid = ["ACCOUNTID"]    # Replace with your AWS account id
  
# Script will look for these tags on the snapshots. It will remove older snapshots with
# tags "BENVIRONMENT":"ENV1" and "BROLE":"ROLE1", or, "BENVIRONMENT":"ENV2" and "BROLE":"ROLE1"

  btags = ["ENV1","ENV2"] 
  brole = ["ROLE1"]
  
  slist = []
  delt = (datetime.date.today().strftime('%Y-%m-%d'))
  regions = ['REGION1','REGION2','REGION3']    # Add all the regions you want to run this script in

  for rg in regions:
    ec2c = session.client('ec2',region_name=rg )
    print ("Searching for " + str(' '.join(btags)) + " " + str(' '.join(brole)) + " snapshots with flag DeleteOn:" \
    + delt + " in " + rg )
    try:
       snapshots = ec2c.describe_snapshots(Filters=[{'Name':'owner-id','Values':ownerid}, \
       {'Name':'status','Values':['completed']},{'Name':'description','Values':['Auto Created by Lambda']}, \
       {'Name':'tag:BENVIRONMENT','Values':btags},{'Name':'tag:BROLE','Values':brole}, \
       {'Name':'tag:DeleteOn','Values':[delt]}]).get('Snapshots')
       
    except Exception as error:
       print ("Can't get the snapshot list. ERROR: " + str(error))
       exit()

    if not snapshots:
      print ("Can't find any!")
    else:
      print ("Found some snapshots! Details to follow")
      for s in snapshots:
        try:
          resp = ec2c.delete_snapshot(SnapshotId=s.get('SnapshotId'))
          print ("Deleted " + str(s.get('SnapshotId')))
          slist.append(s.get('SnapshotId'))
        except Exception as error:
          print ("Can't delete the snapshot. " + str(s.get('SnapshotId')) + "ERROR: " + str(err))
          exit()
  notify(event["topic"],slist,session)
  print ("Execution complete!")
