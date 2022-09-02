from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_lambda_event_sources,
    aws_events,
    aws_events_targets
)
from constructs import Construct

class Awscdktest2Stack(Stack):
    """
    Class to define flow of:
        Event (every minute) -> SQS queue batch -> Lambda running on each batch
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
            self,
            "TestQueue",
        )

        # Send records to lambda after either 3 are in queue or 5 mins pass
        event_source = aws_lambda_event_sources.SqsEventSource(
            queue,
            batch_size=3,
            max_batching_window=Duration.minutes(5)
        )

        event_target = aws_events_targets.SqsQueue(
            queue,
            # This goes to the 'body' of the 'Record' in the event sent to the lambda
            message=aws_events.RuleTargetInput.from_object({"TestParam": "test trigger value"})
        )

        aws_events.Rule(
            self,
            "ScheduleRule",
            schedule=aws_events.Schedule.rate(Duration.minutes(1)),
            targets=[event_target]
        )

        fn = _lambda.Function(
            self,
            'testlambda',
            runtime=_lambda.Runtime.PYTHON_3_9,
            function_name='testlambda',
            description='Test lambda for cdk experimentation',
            code=_lambda.Code.from_asset("./lambdas"),
            handler='lambda_code.handler1',
        )

        fn.add_event_source(event_source)