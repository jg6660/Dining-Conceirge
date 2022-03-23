import json
import boto3
import random
from datetime import datetime, timezone,timedelta

sqs_client = boto3.client('sqs')
queue_url = "https://sqs.us-east-1.amazonaws.com/727641254200/LexQueue"

def send_message(city_name,cuisine,people,number,time,date_input):
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        DelaySeconds=5,
        MessageAttributes={
            'Location': {
                'DataType': 'String',
                'StringValue': city_name
            },
            'Cuisine': {
                'DataType': 'String',
                'StringValue': cuisine
            },
            'People': {
                'DataType': 'Number',
                'StringValue': "{}".format(people)
            },
            'Time': {
                'DataType': 'String',
                'StringValue': time
            },
            'Number': {
                'DataType': 'Number',
                'StringValue': "{}".format(number)
            },
            'Date_input':{
                'DataType': 'String',
                'StringValue': date_input
            }
            
        },
        MessageBody=(
            'Values filled in by the customer.'
        )
    )
    

def lambda_handler(event, context):
    # TODO implement
    print(event)
    intent_name = event.get("currentIntent").get("name")
    

    if intent_name == "GreetingIntent":
        response = "Hey, how can I help you today?"
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": response
                }
            }
        }
    if intent_name == "ThankYouIntent":
        response = "It was a pleasure assisting you. Have a great time!"
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": response
                }
            }
        }

    if intent_name == "DiningSuggestionsIntent":
        slots = event['currentIntent']['slots']
        print("harshitha",slots)
        city_name = event.get("currentIntent").get("slots").get("Location")
        cuisine = event.get("currentIntent").get("slots").get("Cuisine")
        people = event.get("currentIntent").get("slots").get("people")
        date_input = event.get("currentIntent").get("slots").get("Date_input")
        time = event.get("currentIntent").get("slots").get("DiningTime")
        number = event.get("currentIntent").get("slots").get("number")

        response = "It was a pleasure assisting you. Have a great time!"
        time_now = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now(timezone(timedelta(hours=-5), 'EST')))
        time_current = time_now.split(" ")[1]
        hh_mm_ss = time_current.split(":")
        date_current = time_now.split(" ")[0]
        date_parts_current = date_current.split("-")
        d1 = datetime(int(date_parts_current[0]), int(date_parts_current[1]), int(date_parts_current[2])) #current date
        
        if time is not None:
            hh_mm = time.split(":")
        
        if date_input is not None:
            date_parts = date_input.split("-")
            d2 =datetime(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))
            
        if city_name is None:
            message = "What city are you in ?"
            slotToEl = "Location"
            
        elif cuisine is None:
            message = "What type of Cuisine are you looking for?"
            slotToEl = "Cuisine"

        elif people is None:
            message = "How many people are in your party?"
            slotToEl = "people"
            
        elif people is not None and (int(people)==0 or int(people)>20):
            message = "How many people are in your party?(1-20)"
            slotToEl = "people"
        
        elif date_input is None:
            message = "For what date?"
            slotToEl = 'Date_input'
        
        elif date_input is not None and (d1>d2):
            message = "Please enter a valid date. (Date greater than or equal to today)"
            slotToEl = "Date_input"

        elif time is None:
            message = "What time would you like to be seated?"
            slotToEl = "DiningTime"
            
        elif ((d1==d2) and (time is not None) and (int(hh_mm[0])<int(hh_mm_ss[0])) or (int(hh_mm[0])==int(hh_mm_ss[0]) and int(hh_mm[1])<int(hh_mm_ss[1]))):
            message = "Please enter a valid time (greater than current time)."
            slotToEl = "DiningTime"
        
        elif number is None:
            message = "What is your contact number? (Please enter 10 digit US mobile number)"
            slotToEl = "number"
            
        elif number is not None and len(number)<10:
            message = "Please enter 10 digit US mobile number"
            slotToEl = "number"
        
        else:
            send_message(city_name,cuisine,people,number,time,date_input)
            front_response = "We have received your request. You will receive a text shortly"
            return {
                "dialogAction": {
                    "type": "Close",
                    "fulfillmentState": "Fulfilled",
                    "message": {
                        "contentType": "PlainText",
                        "content": front_response
                    }
                }
            }
        slots = event['currentIntent']['slots']
        return {
            "dialogAction": {
                "type": "ElicitSlot",
                "message": {
                  "contentType": "PlainText",
                  "content": message
                },
            "intentName": "DiningSuggestionsIntent",
            "slots": slots,
            "slotToElicit" : slotToEl
            }
        }
            
        