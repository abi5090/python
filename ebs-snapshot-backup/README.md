# EBS Snapshot Backups and Cleanup
Use `ebs-snapshot-backup.py` script to take snapshots of EBS volumes attached to instances with specific tags (controlled via btags and brole variables in the script)

It will take snapshots and tag the snapshots with a "DeleteOn" key, with value of current + 90 days. This tag is then read by the `ebs-snapshot-cleanup.py` script to remove snapshots in the account which are older than 90 days.

Both the scripts can be scheduled to run from AWS Lambda, which should have a role with appropriate permissions.
