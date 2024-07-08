import boto3
import json
import uuid
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from boto3.dynamodb.conditions import Key
import re
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
sns_client = boto3.client('sns', region_name='eu-central-1')
cognito_client = boto3.client('cognito-idp', region_name='eu-central-1')
DYNAMODB_TABLE_NAME = 'MoviesCDK'
ACTORS_TABLE_NAME = 'ActorsCDK'
GENRES_TABLE_NAME = 'GenresCKD'
S3_BUCKET_NAME = 'cloud-movies-cdk'
S3_FOLDER_PATH = 'movies/'
SUBSCRIPTIONS_TABLE_NAME = 'SubscriptionsCDK'

USER_POOL_ID = 'eu-central-1_mN8CW8msb'


def sanitize_topic_name(topic_name):
    # Replace invalid characters with underscores
    sanitized_name = re.sub(r'[^a-zA-Z0-9-_]', '_', topic_name)
    # Ensure the name is within the allowed length
    return sanitized_name[:256]


def get_existing_topic_arn(topic_name):
    next_token = None
    while True:
        if next_token:
            response = sns_client.list_topics(NextToken=next_token)
        else:
            response = sns_client.list_topics()

        for topic in response['Topics']:
            topic_arn = topic['TopicArn']
            if topic_arn.split(':')[-1] == topic_name:
                return topic_arn

        next_token = response.get('NextToken')
        if not next_token:
            break
    return None


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


def publish_to_sns(subject, topic_arn, message):
    response = sns_client.publish(
        TopicArn=topic_arn,
        Subject=subject,
        Message=message
    )


def notify_users(title, actors, director, genres):
    subscription_table = dynamodb.Table(SUBSCRIPTIONS_TABLE_NAME)
    actors_array = [actor.strip() for actor in actors.split(',')]
    genres_array = [genre.strip() for genre in genres.split(',')]

    values = actors_array + genres_array + [director]
    subscribers = []
    message = f"NEW MOVIE: {title}"
    for value in values:
        response = subscription_table.query(
            IndexName="subscription-index",
            KeyConditionExpression=Key('subscription').eq(value)
        )
        for res in response['Items']:
            username = res['username']
            if username not in subscribers:
                topic_name = sanitize_topic_name(res['subscription'])
                topic_arn = get_existing_topic_arn(topic_name)
                print("TOPIC ARN: ", topic_arn)
                publish_to_sns("New movie!", topic_arn, message)
                subscribers.append(username)


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
