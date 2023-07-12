from email import message
import json
from urllib import response
import boto3
import random
from opensearchpy import OpenSearch, RequestsHttpConnection
from aws_requests_auth.aws_auth import AWSRequestsAuth

queue_url = "https://sqs.us-east-1.amazonaws.com/727641254200/LexQueue"
sqs = boto3.client('sqs')
sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')


access_key = ""
secret_key = ""
host = "search-searchdomain-ko7qzpgwxn2ccfufojsvmpegd4.us-east-1.es.amazonaws.com"
region = 'us-east-1'
service = "es"

def send_suggetions(Messages,modifiedNumber):
    messageSent = sns.publish(
        PhoneNumber= modifiedNumber,
        Message= Messages,
        )

def delete_queue_message(message):
    receipt_handle = message['ReceiptHandle']
    sqs.delete_message(
    QueueUrl=queue_url,
    ReceiptHandle=receipt_handle)
    
def get_queue_message():
    response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=1,
    MessageAttributeNames=[
        'All'
    ],
    VisibilityTimeout=0,
    WaitTimeSeconds=0)
    return response

def query_es(response,es):
    message = response['Messages'][0]
    cuisine = message['MessageAttributes'].get('Cuisine').get('StringValue')
    number = message['MessageAttributes'].get('Number').get('StringValue')
    print("phonenumber")
    print(number)
    modifiedNumber = "+1{}".format(number)

    res = es.search(index="restaurants", body={"query": {"match": {"cuisine": cuisine}}})
    return res,modifiedNumber,message

def get_info_DB(res):
    candidates = []
    for entry in res['hits']['hits']:
        candidates.append(entry["_source"])
    ids = []
    for c in candidates:
        ids.append(c.get("id"))
    return ids
    
def draft_message(ids_five):
    j=1
    Messages = "I recommend going to: "
    for i in ids_five:
        #temp_id = restaurant_suggestion
        temp_id = i

        # query DynamoDb table to get more info
        table = dynamodb.Table('yelp-restaurants')
        info = table.get_item(
        Key={
            'id': temp_id,
            }
        )
        Rating = info["Item"]["rating"]
        Name = info["Item"]["name"]
        RatingCount = info["Item"]["review_count"]
        Address = " ".join(info["Item"]["location"])
        Zip = info["Item"]["zipcode"]  ##add this later janu
        ResNum = info['Item']["phone"]
        # message to send to customer
        finalMessage = """ {} ) {}. It has {} reviews with an average {} rating. The address is: {}. Call {} to contact the restaurant and make a booking.\n\n""".format(j,Name, RatingCount, Rating, Address, ResNum) #include ,finZip
        Messages+=finalMessage
        j+=1
    return Messages


def lambda_handler(event, context):
    try:
        awsauth = AWSRequestsAuth(aws_access_key = access_key, aws_secret_access_key = secret_key,
            aws_region = region, aws_service = service, aws_host = host)
    
        es = OpenSearch(hosts = [{'host': host, 'port': 443}],
                           http_auth = awsauth, use_ssl = True,
                           verify_certs = True, connection_class = RequestsHttpConnection)
        
        # sending desired cuisine to query elastic
        response = get_queue_message()
        res,modifiedNumber,message = query_es(response,es)
        ids = get_info_DB(res)
        ids_five = ids[:5]
        Messages = draft_message(ids_five)
        # Send a SMS message to the specified phone number
        send_suggetions(Messages,modifiedNumber)
        # Deleting the SQS Entry
        delete_queue_message(message)
        return {
            'statusCode': 200,
            'body': Messages
        }

    except:
        return {
            'statusCode': 200,
            'body': "No Messages in the queue"
        }
