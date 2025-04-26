import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_janitor.aws_janitor_stack import AwsJanitorStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_janitor/aws_janitor_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsJanitorStack(app, "aws-janitor")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
