import os
import boto3


session = boto3.Session(
    profile_name='iamadmin-production', 
    region_name='us-east-1'  
)
dynamodb = session.resource(
    'dynamodb',
    aws_access_key_id=os.getenv('aws_access_key_id'),
    aws_secret_access_key=os.getenv('aws_secret_access_key_id'))

TableName = dynamodb.Table('serverlessMovieApiTable')

# Define the list of movies with their title, releaseYear, genre and coverUrl
movies = [
    {
        "title": "Bad Boys 2",
        "releaseYear": 2003,
        "genre": "Action",
        "coverUrl": "s3://serverlessmovieapibucket/movieCovers/bad_boys_2.jpg"
    },
    {
        "title": "Coach Carter",
        "releaseYear": 2005,
        "genre": "Sports",
        "coverUrl": "s3://serverlessmovieapibucket/movieCovers/coach_carter.jpg"
    },
    {
        "title": "Dragon Ball Z: Fusion Reborn",
        "releaseYear": 1995,
        "genre": "Anime",
        "coverUrl": "s3://serverlessmovieapibucket/movieCovers/dragon_ball_z_fusion_reborn.jpg"
    },
    {
        "title": "Hidden Figures",
        "releaseYear": 2016,
        "genre": "History",
        "coverUrl": "s3://serverlessmovieapibucket/movieCovers/hidden_figures.jpg"
    },
    {
        "title": "Love and Basketball",
        "releaseYear": 2000,
        "genre": "Romance",
        "coverUrl": "s3://serverlessmovieapibucket/movieCovers/love_and_basketball.jpg"
    },
    {
        "title": "Pokemon: The First Movie",
        "releaseYear": 1998,
        "genre": "Anime",
        "coverUrl": "s3://serverlessmovieapibucket/movieCovers/pokemon_the_first_movie.jpg"
    },
    {
        "title": "Terminator 2: Judgment Day",
        "releaseYear": 1991,
        "genre": "Sci-Fi",
        "coverUrl": "s3://serverlessmovieapibucket/movieCovers/terminator_2.jpg"
    },
    {
        "title": "The Dark Knight",
        "releaseYear": 2008,
        "genre": "Action",
        "coverUrl": "s3://serverlessmovieapibucket/movieCovers/the_dark_knight.jpeg"
    },
    {
        "title": "Toy Story 2",
        "releaseYear": 1999,
        "genre": "Animation",
        "coverUrl": "s3://serverlessmovieapibucket/movieCovers/toy_story.jpeg"
    },
    {
        "title": "Your Name",
        "releaseYear": 2016,
        "genre": "Anime",
        "coverUrl": "s3://serverlessmovieapibucket/movieCovers/your_name.jpeg"
    }
]


with TableName.batch_writer() as batch:
    for item in movies:
        response = batch.put_item(Item={
            "title": item["title"],
            "releaseYear": item["releaseYear"],
            "genre": item["genre"],
            "coverUrl": item["coverUrl"]
        })

# response = TableName.put_item(
#     Item={
#         "title": "Bad Boys 2",
#         "releaseYear": 2003,
#         "genre": "Action",
#         "coverUrl": "https://serverlessmovieapibucket.s3.amazonaws.com/movieCovers/bad_boys_2.jpg"
#     }
# )

print("Movies added to the table")
