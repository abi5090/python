# RDS backup scipt

![py](https://github.com/abiydv/ref-docs/blob/master/images/logos/python_small.png)
![cli](https://github.com/abiydv/ref-docs/blob/master/images/logos/aws-cli_small.png)
![rds](https://github.com/abiydv/ref-docs/blob/master/images/logos/aws-rds_small.png)

Automate the manual snapshot for RDS using Cloudwatch Event rules + Lambda

Script accepts input as json - DB Name, and initiates a snapshot.

To schedule it, create a cloudwatch event rule (cron) that triggers the lambda

	1. Create IAM policy and role with lambda-iam.json
	2. Create Lambda with rds-snapshot-backup.py script
	3. Create Cloudwatch event to execute every 1 day 
	4. Add the lambda (created in 2) as the target to this rule (created in 3)

