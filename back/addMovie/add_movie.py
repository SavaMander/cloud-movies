import boto3
import json
import urllib.parse
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

DYNAMODB_TABLE_NAME = 'Movies'
S3_BUCKET_NAME = 'cloud-movies'
S3_FOLDER_PATH = 'movies/'

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

        table = dynamodb.Table(DYNAMODB_TABLE_NAME)
        item = {
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
        
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': S3_BUCKET_NAME, 'Key': f"{S3_FOLDER_PATH}{title}"},
            ExpiresIn=3600
        )

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
