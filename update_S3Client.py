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

# List of all folders
all_files = ["movieCovers/bad_boys_2.jpg", "movieCovers/coach_carter.jpg",
             "movieCovers/dragon_ball_z_fusion_reborn.jpg","movieCovers/hidden_figures.jpg",
             "movieCovers/love_and_basketball.jpg","movieCovers/pokemon_the_first_movie.jpg",
             "movieCovers/terminator_2.jpg","movieCovers/the_dark_knight.jpeg",
             "movieCovers/toy_story_2.jpeg","movieCovers/your_name.jpeg"]

# Loop through all files and upload them to s3
for x in all_files:
    with open(x, "rb") as f:
        client.upload_fileobj(f, "serverlessmovieapibucket", x)

