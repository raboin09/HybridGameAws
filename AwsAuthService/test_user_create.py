import boto3

client = boto3.client('cognito-idp')

app_client_id = "3q9onjb2p1an8ea2t3sj6c0vq3"
user_pool_id = "us-east-1_2C7BXKazu"
username = "raboin09"
password = "zaq1xsw2ZAQ!XSW@"

resp3 = client.admin_initiate_auth(
    UserPoolId=user_pool_id,
    ClientId=app_client_id,
    AuthFlow="ADMIN_NO_SRP_AUTH",
    AuthParameters={
        "USERNAME": username,
        "PASSWORD": password
    }
)

print("Log in success")
print("Access token:", resp3['AuthenticationResult']['AccessToken'])
print("ID token:", resp3['AuthenticationResult']['IdToken'])