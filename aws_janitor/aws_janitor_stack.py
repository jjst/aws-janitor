import os
from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as targets,
    aws_logs as logs,
)
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from constructs import Construct


class AwsJanitorStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        env = os.environ.get("ENV", "").lower()
        if env not in ["test", "live"]:
            raise ValueError("Please set ENV to 'test' or 'live'")

        self.tags.set_tag("Environment", env)

        if env == "test":
            self.tags.set_tag("TTL", "3 days")

        # === Create the Lambda function ===
        janitor_function = PythonFunction(
            self, "JanitorFunction",
            entry="lambda/janitor",
            runtime=_lambda.Runtime.PYTHON_3_12,
            index="handler.py",
            handler="lambda_handler",
            function_name=f"aws-janitor-function-{env}",
            environment={"ENV": env},
            log_retention=logs.RetentionDays.SIX_MONTHS,
            timeout=Duration.seconds(60),
        )

        # === IAM permissions ===
        actions = ["cloudformation:ListStacks", "cloudformation:DescribeStacks"]
        if env == "live":
            actions.append("cloudformation:DeleteStack")

        janitor_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=actions,
                resources=["*"],
            )
        )

        # === Create EventBridge schedule to trigger Lambda ===
        rule = events.Rule(
            self, "JanitorScheduleRule",
            schedule=events.Schedule.rate(Duration.hours(1)),
            rule_name=f"aws-janitor-schedule-{env}",  # Explicit naming
        )

        rule.add_target(targets.LambdaFunction(janitor_function))
