# Managing AWS with Python
Repository for managing AWS by Python.
The scripts are for testing and learning purpose.


https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
https://click.palletsprojects.com/en/7.x/

## 01 - webotron

Webotron is a script that will sync a local directory to an S3 bucket, and configure Route53 and cloudfront

### Features

Webotron currently has the following features:

- List bucket
- List contents of a bucket
- Create and set up bucket
- Sync directory tree to bucket
- Set AWS profile with --profile= <profileName>
- Configure DNS with Route53
- Publish to Cloud Front with SSL support

### Todos

- Delete bucket
- Delete remote files if not exist in local

## 02 - Notifications

Notifon is a project to notify slack users of changes to your AWS account using CloudWatch events

- EC2 key pair
### Features
