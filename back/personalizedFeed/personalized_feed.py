import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
MOVIES_TABLE = 'Movies'
SUBSCRIPTIONS_TABLE = 'Subscriptions'

def get_user_subscriptions(username):
    table = dynamodb.Table(SUBSCRIPTIONS_TABLE)
    response = table.query(
        IndexName='username-index',
        KeyConditionExpression=Key('username').eq(username)
    )
    return [item['subscription'] for item in response['Items']]

def get_movies_by_subscriptions(subscriptions):
    table = dynamodb.Table(MOVIES_TABLE)
    movies = []
    for subscription in subscriptions:
        response = table.scan(
            FilterExpression=Attr('genres').contains(subscription) | 
                              Attr('actors').contains(subscription) | 
                              Attr('director').eq(subscription)
        )
        movies.extend(response['Items'])
    return movies

def lambda_handler(event, context):
    username = event['pathParameters']['username']
    
    subscriptions = get_user_subscriptions(username)
    personalized_movies = get_movies_by_subscriptions(subscriptions)
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(personalized_movies)
    }
