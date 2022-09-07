import json

def default(event, context):
    print(f'Default request {json.dumps(event)}')

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain',
            # For CORS
            'Access-Control-Allow-Origin': '*'
        },
        'body': f'This is my test response (from default)'
    }

def handler1(event, context):
    print(f'Handler1 request {json.dumps(event)}')

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain',
            # For CORS
            'Access-Control-Allow-Origin': '*'
        },
        'body': f'This is my test response (from handler1)'
    }

def handler2(event, context):
    print(f'Handler2 request {json.dumps(event)}')

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain',
            # For CORS
            'Access-Control-Allow-Origin': '*'
        },
        'body': f'This is my test response (from handler2)'
    }