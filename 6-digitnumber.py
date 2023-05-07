import json
import boto3
import random
import string
from datetime import datetime

def lambda_handler(event, context):
    # Get input parameters
    phone_number = event['phone_number']
    password = event['password']
    
    # Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CustomerTable')

    # Check if customer exists
    response = table.get_item(
        Key={
            'phone_number': phone_number
        }
    )

    # If customer does not exist, return error
    if 'Item' not in response:
        return {
            'status': 'error',
            'message': 'Customer not found with phone number: ' + phone_number
        }
    
    # Update customer's phone password in DynamoDB
    table.update_item(
        Key={
            'phone_number': phone_number
        },
        UpdateExpression='SET phone_password = :val',
        ExpressionAttributeValues={
            ':val': password
        }
    )

    # Generate a unique filename for the text file
    filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + '.txt'
    
    # Connect to S3
    s3 = boto3.resource('s3')
    bucket_name = 'my-s3-bucket'
    bucket = s3.Bucket(bucket_name)

    # Create a text file in S3
    file_content = f"Password for phone number {phone_number}: {password}"
    file_size = len(file_content)
    bucket.put_object(Key=filename, Body=file_content)

    # Update the customer's record in DynamoDB with the file name, size, and timestamp
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    table.update_item(
        Key={
            'phone_number': phone_number
        },
        UpdateExpression='SET file_name = :name, file_size = :size, timestamp = :time',
        ExpressionAttributeValues={
            ':name': filename,
            ':size': file_size,
            ':time': now
        }
    )

    return {
        'status': 'success',
        'message': f"Password for phone number {phone_number} has been updated and a file has been created in S3 with filename {filename}."
    }
