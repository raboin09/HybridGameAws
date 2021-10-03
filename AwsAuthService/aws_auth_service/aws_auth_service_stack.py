import collections

from aws_cdk import (
    core as cdk,
    aws_cognito
)

from aws_cdk.aws_cognito import PasswordPolicy, SignInAliases, StandardAttributes, StandardAttribute


class AwsAuthServiceStack(cdk.Stack):
    # Cognito inputs
    COG_USER_POOL_ID = "cognito_userpool_id"
    COG_USER_POOL_NAME = "GameServiceUserPool"
    COG_PASSWORD_POLICY = PasswordPolicy()
    COG_SIGNIN_ALIASES = SignInAliases(username=True)
    COG_STANDARD_ATTRIBUTES = StandardAttributes()
    COG_SELF_SIGNUP_ENABLED = True
    COG_SIGNIN_CASE_SENSITIVE = True
    COG_LAMBDA_TRIGGERS = aws_cognito.UserPoolTriggers()

    COG_DOMAIN_NAME = "ug-auth"
    COG_DOMAIN_ID = "cognito_domain_id"
    COG_DOMAIN_OPTIONS = aws_cognito.CognitoDomainOptions(domain_prefix=COG_DOMAIN_NAME)

    COG_APP_AUTH_FLOWS = aws_cognito.AuthFlow(user_password=True, admin_user_password=True)
    COG_APPID_ID = "cognito_appid_id"
    COG_APP_NAME = "gamelift-userpool-app"
    COG_APP_GENERATE_SECRET = False

    COG_APP_OAUTH_FLOWS = aws_cognito.OAuthFlows(authorization_code_grant=True)
    COG_APP_OAUTH_SCOPES = [aws_cognito.OAuthScope.EMAIL,
                            aws_cognito.OAuthScope.COGNITO_ADMIN,
                            aws_cognito.OAuthScope.PHONE,
                            aws_cognito.OAuthScope.OPENID,
                            aws_cognito.OAuthScope.PROFILE]
    COG_APP_OAUTH_CALLBACK_URL = ["https://www.google.com"]
    COG_APP_OAUTH_LOGOUT_URL = ["https://www.bing.com"]
    COG_APP_OAUTH = aws_cognito.OAuthSettings(flows=COG_APP_OAUTH_FLOWS,
                                              scopes=COG_APP_OAUTH_SCOPES,
                                              callback_urls=COG_APP_OAUTH_CALLBACK_URL,
                                              logout_urls=COG_APP_OAUTH_LOGOUT_URL)

    def create_cognito_user_pool(self):
        return aws_cognito.UserPool(self,
                                    id=self.COG_USER_POOL_ID,
                                    password_policy=self.COG_PASSWORD_POLICY,
                                    self_sign_up_enabled=self.COG_SELF_SIGNUP_ENABLED,
                                    sign_in_aliases=self.COG_SIGNIN_ALIASES,
                                    sign_in_case_sensitive=self.COG_SIGNIN_CASE_SENSITIVE,
                                    standard_attributes=self.COG_STANDARD_ATTRIBUTES,
                                    user_pool_name=self.COG_USER_POOL_NAME,
                                    lambda_triggers=self.COG_LAMBDA_TRIGGERS
                                    )

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cognito_user_pool = self.create_cognito_user_pool()
        cognito_user_pool.add_domain(id=self.COG_DOMAIN_ID, cognito_domain=self.COG_DOMAIN_OPTIONS)
        cognito_user_pool.add_client(id=self.COG_APPID_ID,
                                     user_pool_client_name=self.COG_APP_NAME,
                                     generate_secret=self.COG_APP_GENERATE_SECRET,
                                     auth_flows=self.COG_APP_AUTH_FLOWS,
                                     o_auth=self.COG_APP_OAUTH
                                     )
