import boto3
import json
from boto3.dynamodb.conditions import Key
from decimal import Decimal

# Function to convert non-serializable types (e.g., Decimal) into serializable ones
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    print("Event:", json.dumps(event))  # Log the event for debugging

    # Extract and validate 'releaseYear' query parameter
    release_year = event.get('queryStringParameters', {}).get('releaseyear')

    if not release_year:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "'releaseyear' query parameter is missing."})
        }


    try:
        # Initialize DynamoDB
        db = boto3.resource('dynamodb')
        table = db.Table('serverlessMovieApiTable')

        # Query the table using releaseYear
        response = table.query(
            KeyConditionExpression=Key('releaseYear').eq(int(release_year))
        )

        # Serialize the response to handle DynamoDB's Decimal type
        items = response['Items']

        # Return the result and help resolve CORS errors
        return {
            "statusCode": 200,
            "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET, OPTIONS"
            },
            "body": json.dumps(items, cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
