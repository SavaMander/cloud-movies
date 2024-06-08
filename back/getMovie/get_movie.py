import json
import boto3
import os
import urllib.parse
table_name = "Movies"
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Print the event for debugging
    print("Event:", event)
    
    # Check if pathParameters and title exist in the event
    title=event['pathParameters']['title']
    title=urllib.parse.unquote(title)
    if not title:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing title in path parameters'})
        }
    
    # Get table instance connection
    table = dynamodb.Table(table_name)
    
    try:
        # Get the item from the table
        response = table.get_item(
            Key={
                'title': title
            }
        )
        
        # Check if the item exists in the response
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {
                'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({'error': 'Item not found'})
            }
        
        # Create response body
        body = {
            'data': response['Item']
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                },
            'body': json.dumps(body, default=str)
        }
    except Exception as e:
        print(f"Error getting item from DynamoDB: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                },
            'body': json.dumps({'error': 'Internal server error'})
        }
