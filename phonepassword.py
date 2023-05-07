import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CustomerTable')

    phone_number = event['phone_number']
    phone_password = event['phone_password']

    response = table.update_item(
        Key={
            'phone_number': phone_number
        },
        UpdateExpression='SET phone_password = :val',
        ExpressionAttributeValues={
            ':val': phone_password
        }
    )

    return {
        'status': 'success'
    }
}
