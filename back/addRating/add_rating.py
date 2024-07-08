import boto3
import json
import uuid
import urllib.parse
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
RATINGS_TABLE_NAME = 'Ratings'

def save_rating_to_db(title, rating, username):
    table = dynamodb.Table(RATINGS_TABLE_NAME)
    rating_id = str(uuid.uuid4())

    try:
        table.put_item(
            Item={
                'id': rating_id,
                'title': title,
                'rating': rating,
                'username': username
            }
        )
    except ClientError as e:
        print(f"Error saving rating: {e.response['Error']['Message']}")
        raise e

def lambda_handler(event, context):
    try:
        # Decode title from URL
        title = urllib.parse.unquote(event["pathParameters"]["title"])

        # Parse body to get the rating
        body = json.loads(event['body'])
        rating = body['rating']

        # Get the username from query parameters
        username = event['queryStringParameters']['username']

        # Validate rating
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        
        save_rating_to_db(title, rating, username)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Rating saved successfully!'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    except ValueError as ve:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': str(ve)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'An error occurred while saving the rating.'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Unexpected error: {str(e)}'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
