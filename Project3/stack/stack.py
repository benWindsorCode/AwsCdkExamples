from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda,
    aws_apigateway,
    Duration
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
            handler=default,
            # Optional extras
            integration_options = aws_apigateway.LambdaIntegrationOptions(
                timeout=Duration.seconds(10)
            ),
            # Use this if you want your api to face a public url
            # domain_name = aws_apigateway.DomainNameOptions(
            #     domain_name="YOUR API URL",
            #     certificate=api_certificate
            # ),

            # The below two are required for cors. You must set the cors options and the response of the gateway
            # Along with the Access-Control-Allow-Origin: '*' in the lambda return value
            default_cors_preflight_options = aws_apigateway.CorsOptions(
                allow_origins=aws_apigateway.Cors.ALL_ORIGINS,
                allow_methods=['OPTIONS', 'GET', 'POST', 'PUT', 'DELETE']
            ),
            default_method_options = aws_apigateway.MethodOptions(
                method_responses=[aws_apigateway.MethodResponse(
                    status_code="200",
                    response_models={
                        "application/json": aws_apigateway.Model.EMPTY_MODEL
                    },
                    response_parameters={
                        # "method.response.header.Content-Type": True,
                        "method.response.header.Access-Control-Allow-Headers": True,
                        "method.response.header.Access-Control-Allow-Origin": True,
                        "method.response.header.Access-Control-Allow-Methods": True,
                        # "method.response.header.Access-Control-Allow-Credentials": True
                    }
                )]
            )
        )

        products_api = gateway.root.add_resource("products")
        products_api.add_method("GET", aws_apigateway.LambdaIntegration(handler1))

        names_api = gateway.root.add_resource("names")
        names_api.add_method("GET", aws_apigateway.LambdaIntegration(handler2))
