## Author: Jacob Chesley
##
## Initial API for direct communication between application and RPi
## Last Updated: 1/25/19

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
        topic='Quick_Run',
        qos=1,
        payload=json.dumps({"Open valve": 1})
        )
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }