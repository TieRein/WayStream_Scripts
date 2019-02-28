## Author: Jacob Chesley
##
## API for direct communication between application and RPi
## Last Updated: 2/5/19

import boto3
import credentials
import json

# AWS User Credentials
region = credentials.region
access_key = credentials.access_key
secret_key = credentials.secret_key

client = boto3.client('iot-data', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

def lambda_handler(event, context):
    response = client.publish(
        topic=event['topic'],
        qos=1,
        payload=json.dumps({"device": event['device'], "duration": event['duration']})
        )
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }