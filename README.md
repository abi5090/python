# Python
![py](https://github.com/abiydv/ref-docs/blob/master/images/logos/python_small.png)

Python code snippets for some mundane AWS administrative tasks

## What is where?

### [AMI Backup & Cleanup](./ami-backup-cleanup)
These scripts can be scheduled in AWS Lambda to create automated AMI backups of your EC2 instances. For details, please refer to the readme in the sub-directory.

### [RDS Snapshot Backup](./rds-snapshot-backup)
These scripts can be scheduled in AWS Lambda to create automated snapshot backups of your RDS instances. For details, please refer to the readme in the sub-directory.

### [EBS Snapshot Backup & Cleanup](./ebs-snapshot-backup)
These scripts can be scheduled in AWS Lambda to create snapshots of EBS volumes attached to shortlisted instances (based on the tags). It also cleansup snapshots older than 90 days to avoid excessive EBS costs. For details, please refer to the readme in the sub-directory.
