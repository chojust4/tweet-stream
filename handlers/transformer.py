import io
import json
import boto3
import logging
import urllib.parse
import csv
from config import S3, S3_BUCKET_NAME

# setup logs
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# setup s3 client
s3_client = boto3.client(S3)


def lambda_handler(event, context):
    logger.info("transformer lambda invoked from s3 ...")

    try:
        # get the s3 bucket name and object key
        s3_bucket = event['Records'][0]['s3']['bucket']['name']
        object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

        # get the s3 object
        s3_response = s3_client.get_object(Bucket=s3_bucket, Key=object_key)
        logger.info("successfully got s3 response for bucket = %s and key = %s", s3_bucket, object_key)

        # read response as a string and convert to objects
        body = s3_response['Body'].read().decode('utf-8')
        tweet_list_as_objects = convert_json_to_object(body)

        # extract information from raw tweet data
        transformer = TweetTransformer(tweet_list_as_objects)
        filtered_tweets = transformer.extract_tweet_data()

        # convert filtered tweet list into csv file
        csvIO = convert_csv(filtered_tweets)
        s3_upload_bytes = bytes(csvIO.getvalue().encode('utf-8'))
        csvIO.close()

        s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=object_key+'.csv', Body=s3_upload_bytes)
    except Exception as e:
        logger.error("s3 error occurred")
        raise e


def convert_csv(filtered_tweets):
    csvIO = io.StringIO()
    writer = csv.writer(csvIO)
    # write headers for the csv file
    writer.writerow([
        'tweet_id',
        'created_timestamp',
        'text',
        'username',
        'user_description',
        'user_follower_count',
        'user_friends_count',
        'favorites',
        'retweets',
        'language'
    ])

    # write each tweet as a row in the csv file
    for tweet in filtered_tweets:
        writer.writerow([
            tweet['tweet_id'],
            tweet['created_timestamp'],
            tweet['text'],
            tweet['username'],
            tweet['user_description'],
            tweet['user_follower_count'],
            tweet['user_friends_count'],
            tweet['favorites'],
            tweet['retweets'],
            tweet['language']
        ])

    logger.info("Successfully converted tweet list into csv file")
    return csvIO


def convert_json_to_object(body):
    tweet_list_as_json = body.split('\n')
    tweet_list_as_json.pop()
    tweet_list_as_objects = []

    logger.info("Tweet list: %s", tweet_list_as_json)

    for tweet in tweet_list_as_json:
        tweet_object = json.loads(tweet)
        tweet_list_as_objects.append(tweet_object)

    logger.info("Successfully parsed json strings into objects")
    return tweet_list_as_objects


class TweetTransformer:

    def __init__(self, tweet_list_as_objects):
        self.tweet_list = tweet_list_as_objects

    def extract_tweet_data(self):
        filtered_tweet_data_list = []

        for tweet in self.tweet_list:
            tweet_dict = {
                'tweet_id': tweet['id'],
                'created_timestamp': tweet['created_at'],
                'text': tweet['text'],
                'username': tweet['user']['name'],
                'user_description': tweet['user']['description'],
                'user_follower_count': tweet['user']['followers_count'],
                'user_friends_count': tweet['user']['friends_count'],
                'favorites': tweet['favorite_count'],
                'retweets': tweet['retweet_count'],
                'language': tweet['lang']
            }

            filtered_tweet_data_list.append(tweet_dict)

        return filtered_tweet_data_list
