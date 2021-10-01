from aws_cdk import (
    core as cdk,
    aws_cognito,
    aws_lambda
)

from aws_cdk.aws_cognito import PasswordPolicy, SignInAliases, StandardAttributes, StandardAttribute


def create_sign_in_aliases():
    alias = SignInAliases(username=True)
    return alias


def create_password_policy():
    password_policy = PasswordPolicy()
    return password_policy


class AwsAuthServiceStack(cdk.Stack):
    # Cognito inputs
    COG_USER_POOL_ID = "cognito_userpool_id"
    COG_USER_POOL_NAME = "GameServiceUserPool"
    COG_PASSWORD_POLICY = create_password_policy()
    COG_SIGNIN_ALIASES = create_sign_in_aliases()
    COG_STANDARD_ATTRIBUTES = StandardAttributes(email=StandardAttribute(required=True))
    COG_SELF_SIGNUP_ENABLED = True
    COG_SIGNIN_CASE_SENSITIVE = True

    COG_APP_AUTH_FLOWS = aws_cognito.AuthFlow(user_password=True, admin_user_password=True)
    COG_APPID_ID = "cognito_appid_id"
    COG_APP_NAME = "gamelift-userpool-app"

    # GetSignInResult inputs
    LAMBDA_GETSIGNINRESULT_ID = "lambda_getsigninresult_id"
    LAMBDA_GETSIGNINRESULT_NAME = "Auth_GetSignInResult"
    LAMBDA_GETSIGNINRESULT_RUNTIME = aws_lambda.Runtime.PYTHON_3_8
    LAMBDA_GETSIGNINGRESULT_HANDLER = "cognito_get_signin_result.lambda_handler"
    LAMBDA_GETSIGNINGRESULT_CODE = aws_lambda.Code.asset("./lambda")

    def create_getsignin_lambda_function(self):
        return aws_lambda.Function(self,
                                   id=self.LAMBDA_GETSIGNINRESULT_ID,
                                   runtime=self.LAMBDA_GETSIGNINRESULT_RUNTIME,
                                   handler=self.LAMBDA_GETSIGNINGRESULT_HANDLER,
                                   code=self.LAMBDA_GETSIGNINGRESULT_CODE,
                                   function_name=self.LAMBDA_GETSIGNINRESULT_NAME
                                   )

    def create_cognito_user_pool(self):
        return aws_cognito.UserPool(self,
                                    id=self.COG_USER_POOL_ID,
                                    password_policy=self.COG_PASSWORD_POLICY,
                                    self_sign_up_enabled=self.COG_SELF_SIGNUP_ENABLED,
                                    sign_in_aliases=self.COG_SIGNIN_ALIASES,
                                    sign_in_case_sensitive=self.COG_SIGNIN_CASE_SENSITIVE,
                                    standard_attributes=self.COG_STANDARD_ATTRIBUTES,
                                    user_pool_name=self.COG_USER_POOL_NAME
                                    )

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cognito_user_pool = self.create_cognito_user_pool()
        cognito_user_pool.add_client(id=self.COG_APPID_ID,
                                     user_pool_client_name=self.COG_APP_NAME,
                                     generate_secret=False,
                                     auth_flows=self.COG_APP_AUTH_FLOWS
                                     )

        lambda_get_signin_result = self.create_getsignin_lambda_function()
