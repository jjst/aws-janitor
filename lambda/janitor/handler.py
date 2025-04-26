import boto3
from botocore.exceptions import ClientError
from pytimeparse.timeparse import timeparse
from datetime import datetime, timedelta, timezone

cf = boto3.client('cloudformation')

def parse_ttl(ttl_str):
    seconds = timeparse(ttl_str)
    if seconds is None:
        raise ValueError(f"Invalid TTL format: {ttl_str}")
    return timedelta(seconds=seconds)

def lambda_handler(event, context):
    now = datetime.now(timezone.utc)
    print(f"🕒 Current UTC time: {now.isoformat()}")

    stacks = cf.describe_stacks()['Stacks']
    print(f"🔍 Found {len(stacks)} stacks.")

    for stack in stacks:
        stack_name = stack['StackName']
        creation_time = stack['CreationTime']
        tags = {tag['Key']: tag['Value'] for tag in stack.get('Tags', [])}

        ttl_str = tags.get('TTL')
        if not ttl_str:
            print(f"ℹ️  Stack '{stack_name}' has no TTL tag, skipping.")
            continue

        expiry_time = creation_time + parse_ttl(ttl_str)
        time_until_expiry = expiry_time - now

        print(f"📦 Stack '{stack_name}': Created at {creation_time.isoformat()}, TTL = {ttl_str}, expires at {expiry_time.isoformat()}")

        if now > expiry_time:
            print(f"⚡ Stack '{stack_name}' is expired! Deleting...")
            try:
                cf.delete_stack(StackName=stack_name)
                print(f"✅ DeleteStack call issued for '{stack_name}'.")
            except ClientError as e:
                error_code = e.response['Error']['Code']
                error_message = e.response['Error']['Message']
                print(f"❌ AWS ClientError when deleting '{stack_name}': {error_code} - {error_message}")
                # (Optional: if AccessDenied, could handle differently here)
        else:
            print(f"⏳ Stack '{stack_name}' is not yet expired. Time until expiry: {time_until_expiry}.")
