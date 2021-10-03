import aws_cdk.aws_apigateway
from aws_cdk import (
    core as cdk,
    aws_apigateway,
    aws_lambda
)


class AwsInfrastructureServiceStack(cdk.Stack):
    API_GATEWAY_ID = "ug-restapi"
    API_GATEWAY_NAME = "api-ug-hybrid"

    GET = "GET"
    POST = "POST"

    APPLICATION_JSON = "application/json"

    # GetSignInResult inputs
    LAMBDA_GETSIGNINRESULT_ID = "lambda_getsigninresult_id"
    LAMBDA_GETSIGNINRESULT_NAME = "Auth_GetSignInResult"
    LAMBDA_GETSIGNINRESULT_RUNTIME = aws_lambda.Runtime.PYTHON_3_8
    LAMBDA_GETSIGNINGRESULT_HANDLER = "cognito_get_signin_result.lambda_handler"
    LAMBDA_GETSIGNINGRESULT_CODE = aws_lambda.Code.asset("./lambda")

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        get_signin_result_handler = aws_lambda.Function(self,
                                                        id=self.LAMBDA_GETSIGNINRESULT_ID,
                                                        runtime=self.LAMBDA_GETSIGNINRESULT_RUNTIME,
                                                        handler=self.LAMBDA_GETSIGNINGRESULT_HANDLER,
                                                        code=self.LAMBDA_GETSIGNINGRESULT_CODE,
                                                        function_name=self.LAMBDA_GETSIGNINRESULT_NAME)

        get_signin_result_integration = aws_apigateway.LambdaIntegration(get_signin_result_handler,
                                                                         request_templates={
                                                                             self.APPLICATION_JSON:
                                                                                 '{ "statusCode": "200" }'})

        rest_api = aws_apigateway.RestApi(self, id=self.API_GATEWAY_ID)
        rest_api.root.add_method(self.GET, get_signin_result_integration)
