# AWS EC2 AMI Backup and Cleanup scripts

Use these scripts to schedule automated AMI backups of your EC2 instances. Description of what each script does, follows.

**Backup.py** - It will create an AMI for all the instances in your account which have a tag "Backup". The AMI created is named as "AUTO-\<InstanceName\>\-\<Date\>".

AMI and Snapshots created will have following tags -  
 - Name\: AUTO-\<InstanceName\>\-\<Date\>
 - Delete After\: Today + 7 days

**Cleanup.py** - It will remove old AMI/Snapshots created by Backup.py
             If today \> "Delete After" tag on the AMI, it is deregistered and attached snapshots are removed.

It can be either scheduled from a local VM/EC2 instance/Jenkins or even Lambda. 

Remember to give relevant permissions to the role/user which is used to execute this script

	ec2:describeinstances
	ec2:describeimages
	ec2:createimage
	ec2:createsnapshot
	ec2:createtags
	ec2:deregisterimage
	ec2:deletesnapshot

:warning: Using only the backup script, may result in a large number of AMIs in the account which can cause unnecessary billing. Use the cleanup script to remove older AMIs from your account.
