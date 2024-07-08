import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
SUBSCRIPTIONS_TABLE = 'Subscriptions'

def delete_subscription(username, subscription):
    table = dynamodb.Table(SUBSCRIPTIONS_TABLE)
    try:
        table.delete_item(
            Key={
                'username': username,
                'subscription': subscription
            }
        )
        return True
    except ClientError as e:
        print(f"Error deleting subscription: {e.response['Error']['Message']}")
        return False

def lambda_handler(event, context):
    try:
        username = event['queryStringParameters']['username']
        subscription = event['queryStringParameters']['subscription']
        
        if delete_subscription(username, subscription):
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Subscription deleted successfully.'}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Failed to delete subscription.'}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
   except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'An error occurred while deleting.'}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            }
        }
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Missing required parameter.'}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            }
        }
