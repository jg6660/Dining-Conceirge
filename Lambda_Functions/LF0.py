import json
import boto3

def lambda_handler(event, context):

    message = event.get("messages")[0].get("unstructured").get("text")
    #id = event["requestID"]
    client = boto3.client('lex-runtime')
    response = client.post_text(
        botName='Dining',
        botAlias='DiningConcierge',
        userId= "id",
        inputText= message)
    return {
        'status_code':200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers' : 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'

        },
        'messages': [ {'type': "unstructured", 'unstructured': {'text': response.get("message")}  } ]
    }
