import os
import boto3


session = boto3.Session(
    profile_name='iamadmin-production', 
    region_name='us-east-1'  
)
client = session.client(
    'dynamodb',
    aws_access_key_id=os.getenv('aws_access_key_id'),
    aws_secret_access_key=os.getenv('aws_secret_access_key_id'))

response = client.create_table(
    AttributeDefinitions=[
        {
            'AttributeName': 'title',
            'AttributeType': 'S',
        },
        {
            'AttributeName': 'releaseYear',
            'AttributeType': 'N'
        }
    ],
    TableName='serverlessMovieApiTable',
    KeySchema=[
        {
            'AttributeName': 'releaseYear',
            'KeyType': 'HASH'
        },
        {   'AttributeName': 'title', 
            'KeyType': 'RANGE'
        }
    ],
    BillingMode='PROVISIONED',
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    },
    Tags=[
        {
            'Key': 'project',
            'Value': 'cloud serverless movie api'
        },
    ]
)

response = client.list_tables()
print("Tables:", response['TableNames'])