from aws_cdk import (
    core, aws_dynamodb
)


class AwsGameliftServiceStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        matchmaking_tickets_table = aws_dynamodb.Table(
            self,
            id="matchmaking_tickets",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            )
        )
