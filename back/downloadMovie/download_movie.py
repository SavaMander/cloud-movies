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
        title = event["pathParameters"]["title"]
        encoded_title=urllib.parse.unquote(title)
        
        # Generate a presigned URL for downloading the file
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET_NAME, 'Key': f"{S3_FOLDER_PATH}{encoded_title}"},
            ExpiresIn=3600
        )

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
