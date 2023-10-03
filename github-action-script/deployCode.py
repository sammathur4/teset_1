import boto3
import time
import sys
import argparse
# import requests  # Removed the import for requests
from datetime import datetime

parser = argparse.ArgumentParser()

# Arguments needed to be passed to run this script:
parser.add_argument('--accessID', '-a', help='AWS Access Key ID')
parser.add_argument('--secretKey', '-k', help='AWS Secret Access Key')
parser.add_argument('--reg', help='AWS Region')
parser.add_argument('--app', help='AWS CodeDeploy Application')
parser.add_argument('--repo', '-r', help='Github Repository Name')
parser.add_argument('--commitID', '-c', help='The commit ID that needs to be deployed on the servers')
parser.add_argument('--user', '-u', help='Github User who triggered the workflow')
parser.add_argument('--ref', help='The branch or tag name that triggered the workflow run')
parser.add_argument('--run', help='A unique number for each workflow run within a repository.')

args = parser.parse_args()

client = boto3.client('codedeploy', aws_access_key_id=args.accessID, aws_secret_access_key=args.secretKey,
                      region_name=args.reg)

app = args.app
dp_groups = client.list_deployment_groups(applicationName=app)['deploymentGroups']

revision = {
    'revisionType': 'GitHub',
    'gitHubLocation': {
        'repository': args.repo,
        'commitId': args.commitID
    }
}

# Setup to send notification alerts via POST request
# Removed the notifications setup

# Create AWS deployments for all deployment groups of the application passed in args.app
for group in dp_groups:
    deployment = client.create_deployment(applicationName=app, deploymentGroupName=group, revision=revision)

    dep_status = 'created'
    while dep_status != 'Failed' and dep_status != 'Succeeded':
        print('waiting', dep_status)
        time.sleep(2)
        dep_status = client.get_deployment(deploymentId=deployment['deploymentId'])['deploymentInfo']['status']

    if dep_status == 'Failed':
        error_msg.append({
            "value": "✦ " + group + " - <https://us-east-1.console.aws.amazon.com/codesuite/codedeploy/deployments/"
                                      + deployment['deploymentId'] + "?region=us-east-1|" + deployment['deploymentId'] + ">",
            "short": False
        })

# Removed the final notifications
