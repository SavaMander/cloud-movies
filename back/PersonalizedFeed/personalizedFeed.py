import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
MOVIES_TABLE = 'MoviesCDK'
SUBSCRIPTIONS_TABLE = 'SubscriptionsCDK'
DOWNLOADS_TABLE = 'DownloadsCDK'
RATINGS_TABLE = 'RatingsCDK'


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
        for movie in response['Items']:
            if movie not in movies:
                movies.append(movie)

    return movies


def get_movies_by_downloads(username):
    downloads_table = dynamodb.Table(DOWNLOADS_TABLE)
    movies_table = dynamodb.Table(MOVIES_TABLE)

    # Querying the downloads table to get the list of downloaded movie titles for the user
    response = downloads_table.query(
        IndexName='username-index',
        KeyConditionExpression=Key('username').eq(username)
    )
    downloaded_movie_ids = [item['title'] for item in response['Items']]  # Title is actually an id

    # Using batch_get_item to fetch movie details for the downloaded movies
    if not downloaded_movie_ids:
        return []

    movie_details = []
    try:
        # Batch get items from Movies table
        response = dynamodb.batch_get_item(
            RequestItems={
                MOVIES_TABLE: {
                    'Keys': [{'id': movie_id} for movie_id in downloaded_movie_ids]
                }
            }
        )
        movie_details = response['Responses'][MOVIES_TABLE]
    except ClientError as e:
        print(f"Error fetching movies: {e.response['Error']['Message']}")

    return movie_details


def get_highly_rated_movies(username):
    ratings_table = dynamodb.Table(RATINGS_TABLE)
    movies_table = dynamodb.Table(MOVIES_TABLE)

    response = ratings_table.query(
        IndexName='username-index',
        KeyConditionExpression=Key('username').eq(username)
    )
    highly_rated_movie_ids = [item['title'] for item in response['Items'] if item['rating'] > 3]

    if not highly_rated_movie_ids:
        return []

    movie_details = []
    try:
        response = dynamodb.batch_get_item(
            RequestItems={
                MOVIES_TABLE: {
                    'Keys': [{'id': movie_id} for movie_id in highly_rated_movie_ids]
                }
            }
        )
        movie_details = response['Responses'][MOVIES_TABLE]
    except ClientError as e:
        print(f"Error fetching high-rated movies: {e.response['Error']['Message']}")

    return movie_details


def lambda_handler(event, context):
    try:
        username = event['queryStringParameters']['username']

        subscriptions = get_user_subscriptions(username)
        personalized_movies = get_movies_by_subscriptions(subscriptions)
        downloaded_movies = get_movies_by_downloads(username)
        highly_rated_movies = get_highly_rated_movies(username)

        combined_movies = personalized_movies + [
            movie for movie in downloaded_movies if movie not in personalized_movies
        ] + [
                              movie for movie in highly_rated_movies if
                              movie not in personalized_movies and movie not in downloaded_movies
                          ]

        return {
            'statusCode': 200,
            'body': json.dumps(combined_movies),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'An error occurred while fetching movies.'}),
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