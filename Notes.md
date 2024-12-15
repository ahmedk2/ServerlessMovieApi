# Notes while doing the project

One of the issues I noticed first was having issues with the attribute definition and key schema not matching. I learned only the key fields need to be included and that non key fields/attributes should be added later when inserting data in the table.

I also had issues with retrieving credentials to interact with AWS. I used env vars to help address IAM issues.

Funny error I had when creating the s3 bucket was InvalidLocationConstraint error while creating S3 bucket in us-east-1 region. If you specify location constraint to us-east-1 region AWS errors because that is the default behavior. Although using other regions does not give you the error.

When trying to view the s3 bucket I saw access denied errors. So to resolve it I unblocked public access and set a bucket policy to allow get object action on all objects in the bucket.

After I could load an item in the table I wanted to load a bunch at once so researching I found we can do that via batch item function. Then I looked at examples online and did it myself.

With my lambda function I had errors `unhashable type 'list' python` when trying to return the response similar to how I did locally querying. When doing research the reason why I got that error was because using curly braces in my old code `return { response['Items'] }` creates a set in Python. Dictionaries or lists can't go in a set and that lead to my error. Change the way I return the data helped resolve my error.

new code

```
return {
    "statusCode": 200,
    "body": response['Items']
}
```

Using key value pairs inside the curly braces allowed me to return the data as a dictionary which can hold lists and dictionaries inside of it. Which is expected output from dynamodb query.

URL to get all movies in the database
https://1sxwpeubpk.execute-api.us-east-1.amazonaws.com/prod

I had some confusion as well on how to dynamically query year based on what year people specify in the query parameters.

## Finally got the get movie by year lambda working 

when creating the method used by the resource I needed to enable the Lambda proxy integration.
This will send the request to your Lambda function as a structured event. I came across this watching a random youtube video but it really made me stumped because the lambda function worked when testing in lambda but never when deployed. It turns out the event was not being passed properly. Even though I am using url query parameters I did not need to specify that in the method for my API gateway.

I also came across serialization errors when querying dynamodb from my lambda. I used found a stackoverflow reference to solve the issue

```
Error Response Observed:
{
  "statusCode": 500,
  "body": "{\"error\": \"Object of type Decimal is not JSON serializable\"}"
}

```

I also tested my lambda using the following event

```
{
  "queryStringParameters": {
    "releaseyear": 2016
  }
}
```

Working link to view movies by release year is [here](https://1sxwpeubpk.execute-api.us-east-1.amazonaws.com/prod/getmoviesbyyear?releaseyear=1999)

![alt text](/resources/image.png)


### Making a frontend

When making a frontend and testing locally I had to enable CORS on the API gateway to fetch data. Specifically on each resource. Since I was getting CORS not enabled errors on the browser console log

Although for the sub resource `/getmoviesbyyear` CORS still was not enabled probably when searching movies by release year. I had to add CORS response headers in my lambda function as mentioned in the [AWS docs](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-cors-console.html):

```
When applying the above instructions to the ANY method in a proxy integration, any applicable CORS headers will not be set. 

Instead, your backend must return the applicable CORS headers, such as Access-Control-Allow-Origin
```

I was using lambda proxy integration for this specific API resource `/getmoviesbyyear` so the above made sense but I did not properly take this in until an hour later.
