import json

def handler1(event, context):
    print(f'request {json.dumps(event)}')

    # Recieving data from sqa, you get an array of 'records'
    # each record has a body which is a string (could be string of json) set by sender
    # as well as messageId, attributes and other info

    for record in event['Records']:
        print(record['body'])
        print(record['messageId'])

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': f'This is my test response'
    }