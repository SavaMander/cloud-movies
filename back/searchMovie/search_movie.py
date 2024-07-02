import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

DYNAMODB_TABLE_NAME = 'Movies'
ACTORS_TABLE_NAME = 'Actors'
GENRES_TABLE_NAME = 'Genres'
table = dynamodb.Table(DYNAMODB_TABLE_NAME)
actors_table = dynamodb.Table(ACTORS_TABLE_NAME)
genres_table = dynamodb.Table(GENRES_TABLE_NAME)

def search_movies(search_type, search_term):
    if search_type=="title" or search_type=="description" or search_type=="director":
        response = table.query(
            IndexName=f'{search_type}-index',
            KeyConditionExpression=Key(search_type).eq(search_term)
        )
        return response['Items']
    elif search_type=="actor":
        movies_ids = actors_table.query(
            IndexName="name-index",
            KeyConditionExpression=Key('name').eq(search_term)
            )
        if movies_ids:
            result=[]
            for movie_id in movies_ids["Items"]:
                response = table.query(
                    KeyConditionExpression=Key('id').eq(movie_id["movie"])
                    )
                result=result+response["Items"]
            return result
    elif search_type=="genre":
        movies_ids = genres_table.query(
            IndexName="name-index",
            KeyConditionExpression=Key('name').eq(search_term)
            ) 
        if movies_ids:
            result=[]
            for movie_id in movies_ids["Items"]:
                response = table.query(
                    KeyConditionExpression=Key('id').eq(movie_id["movie"])
                    )
                result=result+response["Items"]
            return result

def lambda_handler(event, context):
    body = json.loads(event['body'])
    search_type = body['type']
    search_term = body['search_term']
    
    results = search_movies(search_type,search_term)
    
    return {
        "statusCode": 200,
        'headers': {
                'Access-Control-Allow-Origin': '*',
            },
        "body": json.dumps(results)
    }