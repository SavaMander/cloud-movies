import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
SUBSCRIPTIONS_TABLE = 'SubscriptionsCDK'

def get_user_subscriptions(username):
    table = dynamodb.Table(SUBSCRIPTIONS_TABLE)
    response = table.query(
        IndexName='username-index',
        KeyConditionExpression=Key('username').eq(username)
    )
    return [item['subscription'] for item in response['Items']]

def lambda_handler(event, context):
    try:
        username = event['queryStringParameters']['username']
        subscriptions = get_user_subscriptions(username)

        return {
            'statusCode': 200,
            'body': json.dumps(subscriptions),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'An error occurred while fetching subscriptions.'}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            }
        }
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Username not provided in request context.'}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Unexpected error: {str(e)}'}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            }
        }
