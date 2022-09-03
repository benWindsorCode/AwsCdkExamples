import json
import requests

def handler1(event, context):
    print(f'request {json.dumps(event)}')

    # N.B.: requests is not by default present for lambdas, so is installed via requirements.txt
    print(f'requests.Request dir: {dir(requests.Request)}')

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': f'This is my test response'
    }