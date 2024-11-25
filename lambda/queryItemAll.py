import boto3

def lambda_handler(event, context):
    
    db = boto3.resource('dynamodb')
    
    TableName = db.Table('serverlessMovieApiTable')
    response = TableName.scan()

    
    return {
        "body": response['Items']  # Properly return as a dictionary
    }