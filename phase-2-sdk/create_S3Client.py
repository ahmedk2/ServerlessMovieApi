import os
import boto3


session = boto3.Session(
    profile_name='iamadmin-production',
    region_name='us-east-1'  
)
client = session.client(
    's3',
    aws_access_key_id=os.getenv('aws_access_key_id'),
    aws_secret_access_key=os.getenv('aws_secret_access_key_id'))

# Specifying location constraint for us-east-1 region led to errors
# Default for creating buckets is us-east-1 so no need to specify region

response = client.create_bucket(
    Bucket='serverlessmovieapibucket'
)

response = client.list_buckets()

# Loop through Bucket array data and print the name inside buckets 
for bucket in response['Buckets']:
    print(bucket['Name'])