#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aws_janitor.aws_janitor_stack import AwsJanitorStack


env = os.environ.get("ENV", "").lower()
if env not in ["test", "live"]:
    raise ValueError("Please set the ENV environment variable to either 'test' or 'live'.")

app = cdk.App()
AwsJanitorStack(app, f"AwsJanitorStack-{env}",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
