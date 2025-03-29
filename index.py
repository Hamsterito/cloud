import json
import boto3
import uuid

dynamodb = boto3.client('dynamodb')
comprehend = boto3.client('comprehend')

def lambda_handler(event, context):
    try:
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'message': 'CORS preflight response'})
            }

        body = json.loads(event.get('body', '{}'))
        review_text = body.get('review')

        if not review_text:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'error': 'Review text - nope'})
            }

        sentiment_response = comprehend.detect_sentiment(Text=review_text, LanguageCode='en')
        sentiment = sentiment_response['Sentiment']

        review_id = str(uuid.uuid4())
        dynamodb.put_item(
            TableName='Feedbacks',
            Item={
                'reviewId': {'S': review_id},
                'reviewText': {'S': review_text},
                'sentiment': {'S': sentiment}
            }
        )

      
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'reviewId': review_id, 'sentiment': sentiment})
        }

    except Exception as e:
        print(f"Error: {str(e)}")  
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': str(e)})
        }
