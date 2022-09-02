import aws_cdk as cdk
import aws_cdk.aws_s3 as s3

class AwscdktestStack(cdk.Stack):

    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        url = "YOUR URL HERE" # e.g. testsite.com

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

        # If just needing cloudfront and no route53 then just use this
        distribution = cdk.aws_cloudfront.Distribution(
            self,
            "CloudfrontDist",
            default_behavior=cdk.aws_cloudfront.BehaviorOptions(origin=cdk.aws_cloudfront_origins.S3Origin(bucket)),
        )

        # If needing route53 then comment out above distribution and use this instead

        # The below was for trying to hook up route53 too
        # Ran into this issue: https://github.com/aws/aws-cdk/issues/2914
        # In summary: certificate creation can take longer than the timeout
        # For cloudfront you must have certificates in us-east-1, so then have to use a DnsValidatedCertificate to
        # get cross regional certificate to work (as I deploy to eu-west-1).
        # One proposed solution is to deploy al to eu-west-1 then just use a noraml 'certificate'. This has less
        # timeout constraints.
        #
        # hosted_zone = cdk.aws_route53.PublicHostedZone(
        #     self,
        #     "HostedZone",
        #     zone_name=url
        # )
        #
        # my_dns_certificate = cdk.aws_certificatemanager.Certificate(
        #     self,
        #     "Certificate",
        #     domain_name=url,
        #     validation=cdk.aws_certificatemanager.CertificateValidation.from_dns(hosted_zone)
        # )
        #
        # # Another attempt - this one has 5 min timeout but takes longer to create so cant be used
        # # my_dns_certificate = cdk.aws_certificatemanager.DnsValidatedCertificate(
        # #     self,
        # #     "mySiteCert",
        # #     domain_name=url,
        # #     hosted_zone=hosted_zone,
        # #     region="us-east-1"
        # # )
        # #
        # viewer_certificate = cdk.aws_cloudfront.ViewerCertificate.from_acm_certificate(my_dns_certificate)
        # distribution = cdk.aws_cloudfront.CloudFrontWebDistribution(
        #     self,
        #     "MyCfWebDistribution",
        #     origin_configs=[cdk.aws_cloudfront.SourceConfiguration(
        #         s3_origin_source=cdk.aws_cloudfront.S3OriginConfig(
        #             s3_bucket_source=bucket
        #         ),
        #         behaviors=[cdk.aws_cloudfront.Behavior(is_default_behavior=True)]
        #     )],
        #     viewer_certificate=viewer_certificate,
        # )
        # cdk.aws_route53.ARecord(
        #     self,
        #     "CdnARecord",
        #     zone=hosted_zone,
        #     target=cdk.aws_route53.RecordTarget.from_alias(cdk.aws_route53_targets.CloudFrontTarget(distribution))
        # )
        #
        # cdk.aws_route53.AaaaRecord(
        #     self,
        #     "CdnAliasRecord",
        #     zone=hosted_zone,
        #     target=cdk.aws_route53.RecordTarget.from_alias(cdk.aws_route53_targets.CloudFrontTarget(distribution))
        # )
