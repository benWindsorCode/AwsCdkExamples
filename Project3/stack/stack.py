from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda,
    aws_apigateway
)
from constructs import Construct

class StackTest(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        default = aws_lambda.Function(
            self,
            'defaultLambda',
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            function_name='default',
            description='Test default for cdk experimentation',
            code=aws_lambda.Code.from_asset("./lambdas"),
            handler='lambda_code.default',
        )

        handler1 = aws_lambda.Function(
            self,
            'handler1Lambda',
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            function_name='handler1',
            description='Test handler1 for cdk experimentation',
            code=aws_lambda.Code.from_asset("./lambdas"),
            handler='lambda_code.handler1',
        )

        handler2 = aws_lambda.Function(
            self,
            'handler2Lambda',
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            function_name='handler2',
            description='Test handler2 for cdk experimentation',
            code=aws_lambda.Code.from_asset("./lambdas"),
            handler='lambda_code.handler2',
        )

        gateway = aws_apigateway.LambdaRestApi(
            self,
            "api",
            # Handles all requests unless they specify a lambda in addMethod
            handler=default
        )

        products_api = gateway.root.add_resource("products")
        products_api.add_method("GET", aws_apigateway.LambdaIntegration(handler1))

        names_api = gateway.root.add_resource("names")
        names_api.add_method("GET", aws_apigateway.LambdaIntegration(handler2))
