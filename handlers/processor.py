import boto3
import logging
import requests
import urllib.parse
from requests_aws4auth import AWS4Auth

# CONFIGURE YOUR AWS REGION HERE
REGION = '...'
ELASTIC_SEARCH = 'es'
S3 = 's3'

# setup logs
logger = logging.getLogger()
logger.setLevel(logging.INFO)

'''
TODO: 
- setup connection with elasticsearch domain
- send POST request with tweet data to elasticsearch endpoint

'''


def lambda_handler(event, context):
    logger.info("processing lambda invoked from s3 ...")

    # setup credentials and clients
    credentials = boto3.Session().get_credentials()
    awsAuth = AWS4Auth(credentials.access_key, credentials.secret_key, REGION, ELASTIC_SEARCH,
                       session_token=credentials.token)
    s3_client = boto3.client(S3)

    try:
        # get the s3 bucket name and object key
        s3_bucket = event['Records'][0]['s3']['bucket']['name']
        object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

        # get the s3 object
        s3_response = s3_client.get_object(Bucket=s3_bucket, Key=object_key)
        logger.info("successfully got s3 response for bucket = %s and key = %s", s3_bucket, object_key)

        body = s3_response['Body'].read()
        logger.info("Tweet csv file: %s, Type: %s", body, type(body))
    except Exception as e:
        logger.error("error processing s3 bucket to elastic search")
        raise e
