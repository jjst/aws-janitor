import boto3
from pytimeparse.timeparse import timeparse
from datetime import datetime, timedelta

cf = boto3.client('cloudformation')

def parse_ttl(ttl_str):
    seconds = timeparse(ttl_str)
    if seconds is None:
        raise ValueError(f"Invalid TTL format: {ttl_str}")
    return timedelta(seconds=seconds)

def lambda_handler(event, context):
    now = datetime.utcnow()
    stacks = cf.describe_stacks()['Stacks']
    for stack in stacks:
        tags = {tag['Key']: tag['Value'] for tag in stack.get('Tags', [])}
        ttl_str = tags.get('TTL')
        if ttl_str:
            creation_time = stack['CreationTime']
            expiry_time = creation_time + parse_ttl(ttl_str)
            if now > expiry_time:
                print(f"Deleting expired stack: {stack['StackName']}")
                cf.delete_stack(StackName=stack['StackName'])
