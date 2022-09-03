from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_s3,
    aws_lambda,
    aws_lambda_event_sources,
    aws_opensearchservice,
    RemovalPolicy,
    BundlingOptions
)
from constructs import Construct

class StackTest(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = aws_s3.Bucket(
            self,
            "DataBucket",
            versioned=True,
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY
        )

        object_created_event = aws_lambda_event_sources.S3EventSource(
            bucket,
            events=[aws_s3.EventType.OBJECT_CREATED]
        )

        # Lambda with 'requirements.txt' - uses local machine docker to create the base image for lambda
        # For more complex setups use 'layers': https://stackoverflow.com/questions/58855739/how-to-install-external-modules-in-a-python-lambda-function-created-by-aws-cdk
        processing_lambda = aws_lambda.Function(
            self,
            "S3EventProcessor",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            function_name="S3EventProcessor",
            description="Process upload events to s3 bucket",
            code=aws_lambda.Code.from_asset(
                "./lambdas",
                bundling=BundlingOptions(
                    image=aws_lambda.Runtime.PYTHON_3_9.bundling_image,
                    command=[
                        "bash", "-c",
                        "pip install --no-cache -r requirements.txt -t /asset-output && cp -au . /asset-output"
                    ]
                )
            ),
            handler="lambda_code.handler1"
        )

        processing_lambda.add_event_source(object_created_event)

        # This could go on ot upload to an opensearch cluster...
        # opensearch_cluster = aws_opensearchservice.Domain(
        #     self,
        #     "Domain",
        #     version=aws_opensearchservice.EngineVersion.OPENSEARCH_1_3,
        #     capacity=aws_opensearchservice.CapacityConfig(
        #         data_node_instance_type='t2.medium.search'
        #     ),
        #     removal_policy=RemovalPolicy.DESTROY
        # )
