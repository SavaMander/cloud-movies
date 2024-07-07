import boto3
import json
import urllib.parse
import uuid
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
sns_client = boto3.client('sns', region_name='eu-central-1')
cognito_client = boto3.client('cognito-idp', region_name='eu-central-1')

DYNAMODB_TABLE_NAME = 'Movies'
ACTORS_TABLE_NAME = 'Actors'
GENRES_TABLE_NAME = 'Genres'
S3_BUCKET_NAME = 'cloud-movies'
S3_FOLDER_PATH = 'movies/'
SUBSCRIPTIONS_TABLE_NAME = 'Subscriptions'

USER_POOL_ID = 'eu-central-1_fQ3JY76by'
TOPIC_ARN = 'arn:aws:sns:eu-central-1:211125485950:CloudMovies'

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

def publish_to_sns(subject, topic_arn, message, email):
    response = sns_client.publish(
        TopicArn=topic_arn,
        Subject=subject,
        Message=message,
        MessageAttributes={
            'email': {
                'DataType': 'String',
                'StringValue': email
            }
        }
    )

def notify_users(title, actors, director, genres):
    subscription_table = dynamodb.Table(SUBSCRIPTIONS_TABLE_NAME)
    actors_array = [actor.strip() for actor in actors.split(',')]
    genres_array = [genre.strip() for genre in genres.split(',')]
    
    values = actors_array + genres_array + [director]
    subscribers = {}
    
    for value in values:
        response = subscription_table.query(
            IndexName="subscription-index",
            KeyConditionExpression=Key('subscription').eq(value)
        ) 
        for res in response['Items']:
            username = res['username']
            if username not in subscribers:
                subscribers[username] = []
            subscribers[username].append(value)
        
    for username, subscriptions in subscribers.items():
        email = get_user_email_by_username(username)
        if email:
            message = f"NEW MOVIE: {title}\n\nYou received this message because you are subscribed to:"
            for subscription in subscriptions:
                message += f"\n- {subscription}"
            publish_to_sns("New movie!", TOPIC_ARN, message, email)

def update_personalized_feeds():
    lambda_client = boto3.client('lambda', region_name='eu-central-1')
    response = lambda_client.invoke(
        FunctionName='personalizedFeed',  # Ensure this matches your function name
        InvocationType='Event',
        Payload=json.dumps({})
    )

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))
        body = json.loads(event['body'])
        title = body['title']
        description = body['description']
        actors = body['actors']
        director = body['director']
        genres = body['genres']
        name = body['name']
        type = body['type']
        size = body['size']
        date_created = body['dateCreated']
        date_modified = body['dateModified']

        id = str(uuid.uuid4())
    
        table = dynamodb.Table(DYNAMODB_TABLE_NAME)
        item = {
            'id': id,
            'title': title,
            'description': description,
            'actors': actors,
            'director': director,
            'genres': genres,
            'name': name,
            'type': type,
            'size': size,
            'date_created': date_created,
            'date_modified': date_modified 
        }
        table.put_item(Item=item)
        
        actors_array = actors.split(',')
        actors_table = dynamodb.Table(ACTORS_TABLE_NAME)
        for actor in actors_array:
            id2 = str(uuid.uuid4())
            actor_strip = actor.strip()
            actor_item = {
                "id": id2,
                'name': actor_strip,
                'movie': id
            }
            actors_table.put_item(Item=actor_item)
            
        genres_array = genres.split(',')
        genres_table = dynamodb.Table(GENRES_TABLE_NAME)
        for genre in genres_array:
            id3 = str(uuid.uuid4())
            genre_strip = genre.strip()
            genre_item = {
                "id": id3,
                "name": genre_strip,
                "movie": id
            }
            genres_table.put_item(Item=genre_item)
        
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': S3_BUCKET_NAME, 'Key': f"{S3_FOLDER_PATH}{id}"},
            ExpiresIn=3600
        )
        
        notify_users(title, actors, director, genres)
        
        # Update personalized feeds after notifying users
        update_personalized_feeds()

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                'message': 'Movie added successfully!',
                'upload_url': presigned_url
            })
        }
    except NoCredentialsError:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Credentials not available'})
        }
    except PartialCredentialsError:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Incomplete credentials provided'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }
