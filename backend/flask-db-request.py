from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from boto3.dynamodb.conditions import Key
import os
from decimal import Decimal

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Set up DynamoDB session
session = boto3.Session(
    region_name='us-east-1'  
)
dynamodb = session.resource(
    'dynamodb',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Connect to the DynamoDB table
table = dynamodb.Table('serverlessMovieApiTable')

# Helper function to handle Decimal type from DynamoDB
def decimal_to_float(data):
    if isinstance(data, list):
        return [decimal_to_float(item) for item in data]
    elif isinstance(data, dict):
        return {key: decimal_to_float(value) for key, value in data.items()}
    elif isinstance(data, Decimal):
        return float(data)
    return data

# Route to get all movies
@app.route('/movies', methods=['GET'])
def get_all_movies():
    try:
        response = table.scan()
        items = decimal_to_float(response['Items'])  # Convert Decimals to floats
        return jsonify(items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get movies by year
@app.route('/movies/<int:year>', methods=['GET'])
def get_movies_by_year(year):
    try:
        response = table.query(
            KeyConditionExpression=Key('releaseYear').eq(year)
        )
        items = decimal_to_float(response['Items'])  # Convert Decimals to floats
        return jsonify(items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)