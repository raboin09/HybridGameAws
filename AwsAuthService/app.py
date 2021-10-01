#!/usr/bin/env python3

from aws_cdk import core
from aws_auth_service.aws_auth_service_stack import AwsAuthServiceStack

# env_USA = core.Environment(account="305148788366", region="us-east-1")

app = core.App()
AwsAuthServiceStack(app, "AwsAuthServiceStack")#, env=env_USA)
app.synth()
