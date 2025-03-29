import json
import boto3
import uuid

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Reviews")
comprehend = boto3.client("comprehend")

def lambda_handler(event, context):
    body = json.loads(event["body"])
    review_text = body.get("review", "")

    if not review_text:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "nope text"})
        }

    sentiment_response = comprehend.detect_sentiment(
        Text=review_text, LanguageCode="en"
    )
    sentiment = sentiment_response["Sentiment"]

    item = {
        "id": str(uuid.uuid4()),
        "review": review_text,
        "sentiment": sentiment
    }

    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "body": json.dumps({"sentiment": sentiment})
    }