# EBS Snapshot Backups and Cleanup

![py](https://github.com/abiydv/ref-docs/blob/master/images/logos/python_small.png)
![cli](https://github.com/abiydv/ref-docs/blob/master/images/logos/aws-cli_small.png)
![ec2](https://github.com/abiydv/ref-docs/blob/master/images/logos/aws-ec2_small.png)
![ebs](https://github.com/abiydv/ref-docs/blob/master/images/logos/aws-ebs_small.png)

These scripts take EBS snapshots based on a tag applied to the instance. Also cleansup old snapshots based on retention policy.

## How to use
Use `ebs-snapshot-backup.py` script to take snapshots of EBS volumes attached to instances with specific tags (controlled via btags and brole variables in the script)

It will take snapshots and tag the snapshots with a "DeleteOn" key, with value of current + 90 days. This tag is then read by the `ebs-snapshot-cleanup.py` script to remove snapshots in the account which are older than 90 days.

Both the scripts can be scheduled to run from AWS Lambda, which should have a role with appropriate permissions.
