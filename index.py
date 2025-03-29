import json
import boto3
import uuid

dynamodb = boto3.client('dynamodb')
comprehend = boto3.client('comprehend', region_name='eu-west-2')

def lambda_handler(event, context):
    try:
        if 'body' in event:
            body = json.loads(event.get('body', '{}'))
        else:
            body = event
        
        review_text = body.get('review')

        if not review_text:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Review text is missing'})
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
            'body': json.dumps({'reviewId': review_id, 'sentiment': sentiment})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }