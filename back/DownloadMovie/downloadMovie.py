import boto3
import json
import uuid
import urllib.parse
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

DYNAMODB_TABLE_NAME = 'DownloadsCDK'
S3_BUCKET_NAME = 'cloud-movies-cdk'
S3_FOLDER_PATH = 'movies/'


def write_download_record(movie_title, username):
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    table.put_item(
        Item={
            'id': str(uuid.uuid4()),
            'title': movie_title,
            'username': username
        }
    )


def lambda_handler(event, context):
    try:
        title = event["pathParameters"]["title"]
        encoded_title = urllib.parse.unquote(title)
        username = event['queryStringParameters']['username']

        # Generate a presigned URL for downloading the file
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET_NAME, 'Key': f"{S3_FOLDER_PATH}{encoded_title}"},
            ExpiresIn=3600
        )

        write_download_record(encoded_title, username)

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                'download_url': presigned_url
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }
