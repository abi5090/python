import boto3
import time

def lambda_handler(event, context):
    db_to_backup = event['dbname']
    snapshot_name = str(db_to_backup) + str(time.strftime("%Y%m%d"))
    client = boto3.client('rds')
    response = client.create_db_snapshot(DBSnapshotIdentifier=snapshot_name,DBInstanceIdentifier=db_to_backup)
    print(response)
