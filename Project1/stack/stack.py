import aws_cdk as cdk
import aws_cdk.aws_s3 as s3

class StackTest(cdk.Stack):

    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(
            self,
            "MyFirstBucket",
            versioned=True,
            auto_delete_objects=True,
            public_read_access=True,
            website_index_document="index.html",
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        cdk.aws_s3_deployment.BucketDeployment(
            self,
            "DeployWebsite",
            destination_bucket=bucket,
            sources=[cdk.aws_s3_deployment.Source.data(
                'index.html',
                """
                <html xmlns="http://www.w3.org/1999/xhtml" >
                    <head>
                        <title>Home Page</title>
                    </head>
                    <body>
                      <h1>Test Website Page</h1>
                      <p>Website hosted via S3 bucket and Cloudfront</p>
                    </body>
                </html>"""
            )],
        )

        # OPTION 1: If just needing cloudfront and no route53 then just use this
        # distribution = cdk.aws_cloudfront.Distribution(
        #     self,
        #     "CloudfrontDist",
        #     default_behavior=cdk.aws_cloudfront.BehaviorOptions(origin=cdk.aws_cloudfront_origins.S3Origin(bucket)),
        # )

        # OPTION 2: If needing route53 then comment out above distribution and use this instead
        # N.B. some setup required:
        # - you need a domain and a hosted zone (ensure the name servers in the domain and hosted zone match!!!)
        # - you need a certificate in us-east-1 (to use cloudfront) that is added to the hosted zone (theres a button on the certificate page to do this)
        hosted_zone_id = "YOUR HOSTED ZONE ID HERE"
        certificate_arn = "YOUR CERTIFICATE ARN HERE"
        url = "YOUR URL HERE"

        hosted_zone = cdk.aws_route53.HostedZone.from_hosted_zone_attributes(
            self,
            "hosted_zone",
            zone_name=url,
            hosted_zone_id=hosted_zone_id
        )

        my_dns_certificate = cdk.aws_certificatemanager.Certificate.from_certificate_arn(
            self,
            "Certificate",
            certificate_arn
        )

        distribution = cdk.aws_cloudfront.Distribution(
            self,
            "MyCfWebDistribution",
            default_behavior=cdk.aws_cloudfront.BehaviorOptions(origin=cdk.aws_cloudfront_origins.S3Origin(bucket)),
            domain_names=[url],
            certificate=my_dns_certificate
        )

        cdk.aws_route53.ARecord(
            self,
            "CdnARecord",
            zone=hosted_zone,
            target=cdk.aws_route53.RecordTarget.from_alias(cdk.aws_route53_targets.CloudFrontTarget(distribution))
        )

        cdk.aws_route53.AaaaRecord(
            self,
            "CdnAliasRecord",
            zone=hosted_zone,
            target=cdk.aws_route53.RecordTarget.from_alias(cdk.aws_route53_targets.CloudFrontTarget(distribution))
        )