import boto3
import json
import datetime

access_key="AKIA2S2WMNE4G7K2H47J"
secret_access_key="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"
session=boto3.Session(aws_access_key_id=access_key,aws_secret_access_key=secret_access_key, region_name='us-east-1')
client_dynamo=session.resource('dynamodb')
table=client_dynamo.Table('yelp-restaurants')
records=""

with open('thai_yelp.json','r') as datafile:
    records = json.load(datafile)
    records = records['businesses']
    #records = records[0]
print(type(records))
print(len(records))

for i in records:
    #print(i)
    del i['distance']
    del i['image_url']
    del i['url']
    datet = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    i['insertedAtTimestamp'] = datet
    del i['categories']
    del i['transactions']
    i['zipcode']=str(i['location']['zip_code'])
    i['location'] = i['location']['display_address']
    del i['display_phone']
    i['cuisine']='thai'
    i['rating']=str(i['rating'])
    i['coordinates'] = str(i['coordinates'])
    print(i)
    response=table.put_item(Item=i)

