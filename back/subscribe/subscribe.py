import json
import uuid
import boto3

SUBSCRIPTIONS_TABLE_NAME='Subscriptions'
TOPIC_ARN = 'arn:aws:sns:eu-central-1:211125485950:CloudMovies'
USER_POOL_ID = 'eu-central-1_fQ3JY76by'
sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')
cognito_client = boto3.client('cognito-idp', region_name='eu-central-1')

def get_user_email_by_username(username):
    try:
        response = cognito_client.admin_get_user(
            UserPoolId=USER_POOL_ID,
            Username=username
        )
        for attribute in response['UserAttributes']:
            if attribute['Name'] == 'email':
                return attribute['Value']
    except cognito_client.exceptions.UserNotFoundException:
        print(f"User {username} not found in pool {USER_POOL_ID}.")
    except Exception as e:
        print(f"An error occurred while retrieving user email: {e}")
    return None

def subscribe_email_to_topic(email, topic_arn):
    response = sns.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=email
    )
    return response

def add_subscription(username, subscription_value):
    table = dynamodb.Table(SUBSCRIPTIONS_TABLE_NAME)
    id=str(uuid.uuid4())
    response = table.put_item(
       Item={
            'id': id,
            'username' : username,
            'subscription': subscription_value,
        }
    )
    return response

def lambda_handler(event, context):
    body = json.loads(event['body'])
    username = body['username']
    subscription_value = body['subscription']
    
    add_subscription(username, subscription_value)
    email = get_user_email_by_username(username)
    if email:
        subscribe_email_to_topic(email, TOPIC_ARN)
    return {
        'statusCode': 200,
        'headers': {
                'Access-Control-Allow-Origin': '*',
            },
        'body': json.dumps('Successfully added subscription!')
    }
