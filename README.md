# aws-janitor

**aws-janitor** is a small AWS CDK project that deploys a scheduled Lambda function to automatically clean up old test stacks in your AWS account.

It uses stack tags (`TTL`) to determine when a stack should be deleted, ensuring that test resources don't linger and accumulate unnecessary costs.

---

## How It Works

- Each CloudFormation stack can be tagged with a `TTL` (e.g., `3 days`).
- The janitor Lambda runs every hour (EventBridge rule).
- It finds stacks whose creation time + TTL has expired.
- Expired stacks are automatically deleted.

The janitor's behavior differs depending on the environment:

- **test**: Can only *read* stacks (no deletions allowed, safe mode).
- **live**: Can *read and delete* expired stacks.

Environment is controlled by the `ENV` environment variable (`test` or `live`).

---

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

---

## Useful Commands

- `cdk ls` — list all stacks
- `cdk synth` — output the synthesized CloudFormation template
- `cdk deploy` — deploy your stack to AWS
- `cdk diff` — compare your stack against deployed version
- `cdk destroy` — destroy the deployed stack

---

## Project Structure

- `app.py` — CDK application entry point
- `aws_janitor/` — CDK stack definition
- `lambda/janitor/handler.py` — Janitor Lambda code
- `requirements.txt` — Python dependencies

---

## Notes

- Lambda log retention is set to **6 months** to minimize costs.
- The janitor is designed to fail safely in test environments.
- Stack tagging is automatic via a shared `BaseStack` from `cdk-tools`.

---

Enjoy clean AWS accounts and predictable cloud costs! ✨

