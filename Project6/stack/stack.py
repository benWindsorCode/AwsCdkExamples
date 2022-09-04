from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_s3,
    aws_apigateway,
    aws_lambda,
    aws_route53,
    aws_route53_targets,
    aws_certificatemanager,
    CfnOutput,
    Duration
)
from constructs import Construct

class StackTest(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Certificate linking hosted zone to domain
        certificate_arn = "YOUR CERTIFICATE ARN HERE"
        url = "YOUR PUBLIC DOMAIN URL HERE"
        hosted_zone_id = "YOUR HOSTED ZONE ID HERE"

        default_handler = aws_lambda.Function(
            self,
            "default_handler",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            function_name="default_handler",
            description="Default handler",
            code=aws_lambda.Code.from_asset(
                "./lambdas",
            ),
            handler="lambda_code.handler1",
            # Env vars for function, access with os.environ['some_var_name']
            environment={
                'some_var_name':'some_env_var',
            },
            timeout=Duration.seconds(10)
        )

        # Note, hosted zone  manually created, Name servers of domain edited to match NS of the hosted zone
        # Once sorted one time only then can you use the below.
        # Requesting a certificate can be automated, though its one time setup so quicker to sort once
        # as it can take up to 5 or so mins to request and to destroy a certificate
        hosted_zone = aws_route53.HostedZone.from_hosted_zone_attributes(
            self,
            "hosted_zone",
            zone_name=url,
            hosted_zone_id=hosted_zone_id
        )

        my_dns_certificate = aws_certificatemanager.Certificate.from_certificate_arn(
            self,
            "Certificate",
            certificate_arn
        )

        gateway = aws_apigateway.LambdaRestApi(
            self,
            "api",
            # Handles all requests unless they specify a lambda in addMethod
            handler=default_handler,
            integration_options=aws_apigateway.LambdaIntegrationOptions(
                timeout=Duration.seconds(10)
            ),
            domain_name=aws_apigateway.DomainNameOptions(
                    domain_name=url,
                    certificate=my_dns_certificate
                )
        )

        gateway.add_usage_plan(
            "throttle_settings_usage_plan",
            throttle=aws_apigateway.ThrottleSettings(
                rate_limit=10,
                burst_limit=5
            ),
            api_stages=[aws_apigateway.UsagePlanPerApiStage(
                api=gateway,
                stage=gateway.deployment_stage
            )]
        )

        aws_route53.ARecord(
            self,
            "zone_target_api_gateway",
            zone=hosted_zone,
            target=aws_route53.RecordTarget.from_alias(aws_route53_targets.ApiGateway(gateway))
        )

        # This adds the value to the output of the cdk call, so it can be shown to user and used by later bash commands etc.
        CfnOutput(
            self,
            "CertificateUsed",
            value=certificate_arn
        )