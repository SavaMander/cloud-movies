import json
import uuid
import boto3
import re

SUBSCRIPTIONS_TABLE_NAME = 'SubscriptionsCDK'
USER_POOL_ID = 'eu-central-1_b7f8mMcH1'
TOPIC_ARN = 'arn:aws:sns:eu-central-1:211125485950:CloudMoviesCDK'
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


def sanitize_topic_name(topic_name):
    # Replace invalid characters with underscores
    sanitized_name = re.sub(r'[^a-zA-Z0-9-_]', '_', topic_name)
    # Ensure the name is within the allowed length
    return sanitized_name[:256]


def subscribe_email_to_topic(email, topic_arn):
    response = sns.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=email
    )
    return response


def add_subscription(username, subscription_value):
    table = dynamodb.Table(SUBSCRIPTIONS_TABLE_NAME)
    id = str(uuid.uuid4())
    response = table.put_item(
        Item={
            'id': id,
            'username': username,
            'subscription': subscription_value,
        }
    )
    return response


def create_topic(topic_name):
    sanitized_name = sanitize_topic_name(topic_name)
    try:
        response = sns.create_topic(Name=sanitized_name)
        return response['TopicArn']
    except Exception as e:
        print(f"An error occurred while creating topic: {e}")
        return None


def get_existing_topic_arn(topic_name):
    next_token = None
    while True:
        if next_token:
            response = sns.list_topics(NextToken=next_token)
        else:
            response = sns.list_topics()

        for topic in response['Topics']:
            topic_arn = topic['TopicArn']
            if topic_arn.split(':')[-1] == topic_name:
                return topic_arn

        next_token = response.get('NextToken')
        if not next_token:
            break
    return None


def lambda_handler(event, context):
    body = json.loads(event['body'])
    username = body['username']
    subscription_value = body['subscription']

    add_subscription(username, subscription_value)
    email = get_user_email_by_username(username)
    if email:
        topic_arn = get_existing_topic_arn(subscription_value)

        if not topic_arn:
            topic_arn = create_topic(subscription_value)
        subscribe_email_to_topic(email, topic_arn)
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps('Successfully added subscription!')
    }
