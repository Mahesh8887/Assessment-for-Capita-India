import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CustomerTable')

    phone_number = event['phone_number']

    response = table.get_item(
        Key={
            'phone_number': phone_number
        }
    )

    if 'Item' not in response:
        return {
            'status': 'customer_not_found'
        }
    elif 'phone_password' not in response['Item']:
        return {
            'status': 'customer_found_no_password'
        }
    else:
        return {
            'status': 'customer_found_with_password'
        }
