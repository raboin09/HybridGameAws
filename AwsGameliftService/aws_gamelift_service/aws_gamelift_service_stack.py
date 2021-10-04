from aws_cdk import (
    core,
    aws_dynamodb,
    aws_iam,
    aws_gamelift,
    aws_s3
)


class AwsGameliftServiceStack(core.Stack):
    POLICY_DOC_JSON = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": ["gamelift:*"],
            "Resource": "*"
        }]
    }

    IAM_GAMELIFT_POLICY_NAME = "IAM_GameLiftFullAccess"
    IAM_GAMELIFT_POLICY_DOC_PARSED = aws_iam.PolicyDocument.from_json(POLICY_DOC_JSON)
    IAM_GAMELIFT_USER_NAME = "UG_GameliftAdmin"

    PARAM_STAGE_ALLOWED_VALUES = ["prod", "staging", "dev"]
    PARAM_STAGE_DESC = "Where to deploy this infrastructure (prod, staging, or dev)"
    PARAM_STAGE_DEFAULT = "dev"

    PARAM_REGION_ALLOWED_VALUES = ["us-east-1"]
    PARAM_REGION_DESC = "What region to deploy to"
    PARAM_REGION_DEFAULT = "us-east-1"

    PARAM_BUILD_LOC_DESC = "Where the build is located"

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Input values when cdk deploy is called
        stage = self.node.try_get_context("stage")
        region = self.node.try_get_context("region")
        build_id = self.node.try_get_context("build_id")
        build_version = self.node.try_get_context("build_version")

        fleet_server_instance_type = self.node.try_get_context("fleet_server_instance_type")
        fleet_os = self.node.try_get_context("fleet_os")
        fleet_type = self.node.try_get_context("fleet_type")
        fleet_name = self.node.try_get_context("fleet_name")
        fleet_concurrent_executions = self.node.try_get_context("fleet_concurrent_executions")
        fleet_launch_path = self.node.try_get_context("fleet_launch_path")
        fleet_launch_params = self.node.try_get_context("fleet_launch_params")

        fleet_name = stage + "-" + fleet_name
        fleet_name += " " + fleet_server_instance_type
        fleet_name += " " + fleet_os
        fleet_name += " " + fleet_type
        fleet_name += " " + build_version

        # Gamelift IAM resources and access/secret key outputs
        gamelift_policy = aws_iam.Policy(self, id="gamelift_iam_policy_id",
                                         policy_name=self.IAM_GAMELIFT_POLICY_NAME,
                                         document=self.IAM_GAMELIFT_POLICY_DOC_PARSED)
        gamelift_user = aws_iam.User(self, id="gamelift_user_id",
                                     user_name=self.IAM_GAMELIFT_USER_NAME,
                                     managed_policies=[gamelift_policy])
        gamelift_user_access_key = aws_iam.CfnAccessKey(self, id="gamelift_user_access_key_id",
                                                        user_name=self.IAM_GAMELIFT_USER_NAME)
        cfn_output_access_key = core.CfnOutput(self, id="cfn_user_access_key_output_id",
                                               value=gamelift_user_access_key.ref)
        cfn_output_secret_key = core.CfnOutput(self, id="cfn_user_secret_key_output_id",
                                               value=gamelift_user_access_key.attr_secret_access_key)

        # Gamelift fleet
        fleet_server_process_1 = aws_gamelift.CfnFleet.ServerProcessProperty(self, id="fleet_server_process_id_1",
                                                                             concurrent_executions=
                                                                             fleet_concurrent_executions,
                                                                             launch_path=fleet_launch_path,
                                                                             parameters=fleet_launch_params + "7777")
        fleet_server_process_2 = aws_gamelift.CfnFleet.ServerProcessProperty(self, id="fleet_server_process_id_2",
                                                                             concurrent_executions=
                                                                             fleet_concurrent_executions,
                                                                             launch_path=fleet_launch_path,
                                                                             parameters=fleet_launch_params + "7778")
        fleet_server_process_3 = aws_gamelift.CfnFleet.ServerProcessProperty(self, id="fleet_server_process_id_3",
                                                                             concurrent_executions=
                                                                             fleet_concurrent_executions,
                                                                             launch_path=fleet_launch_path,
                                                                             parameters=fleet_launch_params + "7779")
        fleet_server_process_4 = aws_gamelift.CfnFleet.ServerProcessProperty(self, id="fleet_server_process_id_4",
                                                                             concurrent_executions=
                                                                             fleet_concurrent_executions,
                                                                             launch_path=fleet_launch_path,
                                                                             parameters=fleet_launch_params + "7780")
        fleet_server_process_5 = aws_gamelift.CfnFleet.ServerProcessProperty(self, id="fleet_server_process_id_5",
                                                                             concurrent_executions=
                                                                             fleet_concurrent_executions,
                                                                             launch_path=fleet_launch_path,
                                                                             parameters=fleet_launch_params + "7781")

        fleet_processes_list = [fleet_server_process_1,
                                fleet_server_process_2,
                                fleet_server_process_3,
                                fleet_server_process_4,
                                fleet_server_process_5]

        fleet_runtime_config = aws_gamelift.CfnFleet.RuntimeConfigurationProperty(self, id="fleet_runtime_id",
                                                                                  game_session_activation_timeout_seconds=600,
                                                                                  server_processes=fleet_processes_list)

        fleet_port_settings_1 = aws_gamelift.CfnFleet.IpPermissionProperty(self, id="port_settings_id_1",
                                                                           from_port=7777,
                                                                           to_port=7781,
                                                                           protocol="UDP",
                                                                           ip_range="0.0.0.0/0")

        gamelift_fleet = aws_gamelift.CfnFleet(self, id="gamelift_fleet_id",
                                               name=fleet_name,
                                               fleet_type=fleet_type,
                                               build_id=build_id,
                                               runtime_configuration=fleet_runtime_config)
