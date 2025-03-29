import json
import boto3
import uuid

dynamodb = boto3.client('dynamodb')
comprehend = boto3.client('comprehend')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    review_text = body['review']
    
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