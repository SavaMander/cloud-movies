import json
import boto3
import os
import urllib.parse

table_name = "MoviesCDK"
bucket_name = 'cloud-movies-cdk'

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')


def lambda_handler(event, context):
    id = event['pathParameters']['title']
    id = urllib.parse.unquote(id)
    if not id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing title in path parameters'})
        }

    table = dynamodb.Table(table_name)

    try:
        response = table.delete_item(
            Key={
                'id': id
            }
        )
        dynamodb_status = 'Item deleted successfully from DynamoDB'
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error deleting item from DynamoDB: ' + str(e))
        }

    try:
        s3.delete_object(Bucket=bucket_name, Key="movies/" + id)
        s3_status = 'Object deleted successfully from S3'
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error deleting object from S3: ' + str(e))
        }

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({
            'message': 'Movie successfully deleted'
        })
    }