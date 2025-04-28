# aws-janitor

**aws-janitor** is a small AWS CDK project that deploys a scheduled Lambda function to automatically clean up old test stacks in your AWS account.

It uses stack tags (`TTL`) to determine when a stack should be deleted, ensuring that test resources don't linger and accumulate unnecessary costs.


## How to Use

1. **Tag your CloudFormation stacks**
   - Add a `TTL` tag to your stack.
   - The value should be human-readable, e.g., `12 hours`, `3 days`, or `30 minutes`.

2. **Automatic Cleanup**
   - The janitor Lambda will regularly scan stacks.
   - If a stack's creation time + TTL is in the past, it will be automatically deleted.

3. **Helpful Tooling**
   - See [aws-cdk-tools](https://github.com/jjst/aws-cdk-tools) for code to automatically add a TTL to your CDK stacks.


## Setup Instructions

1. **Set up your virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set the deployment environment**

```bash
export ENV=test   # or ENV=live
```

4. **Deploy the stack**

```bash
cdk deploy
```


## Useful Commands

- `cdk ls` &mdash; list all stacks
- `cdk synth` &mdash; output the synthesized CloudFormation template
- `cdk deploy` &mdash; deploy your stack to AWS
- `cdk diff` &mdash; compare your stack against deployed version
- `cdk destroy` &mdash; destroy the deployed stack


## Project Structure

- `app.py` &mdash; CDK application entry point
- `aws_janitor/` &mdash; CDK stack definition
- `lambda/janitor/handler.py` &mdash; Janitor Lambda code
- `requirements.txt` &mdash; Python dependencies


## Notes
- Lambda log retention is set to **6 months** to minimize costs.
- The janitor is designed to fail safely in test environments.
- Stack tagging is automatic via a shared `BaseStack` from [aws-cdk-tools](https://github.com/jjst/aws-cdk-tools).


