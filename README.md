### tweet-stream

`tweet-stream` is a simple, serverless data pipeline used to extract and transform live tweets in real time. 

### aws resources

Cloudformation will create the following resources to your stack

**Lambda** 

2 lambda functions will be created; one to process raw data from kinesis firehose, and another to process data into elastic search

**Kinesis Firehose**

Kinesis firehose resource will be created to load data into S3. Buffer times can be configured in `cloudformation_template.yaml`

**S3**

2 S3 buckets will be created; one for raw tweet data as json, and another for filtered data as a csv file

**ElasticSearch**

An elasticsearch domain (es cluster) will be created; details can be found in `cloudformation_template.yaml`

### prerequisites

1. get api keys from the [twitter api](https://developer.twitter.com/en/docs) and specify credentials in `credentials.py`
2. download and configure the [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

### deploying the stack

run `zip-processor-lambda.sh` script to install dependencies and package the lambda function

```shell
cd twitter-data-pipeline
chmod +x ./zip-processor-lambda.sh
./zip-processor-lambda.sh
```

specify S3 bucket and cloudformation stack names in `sam-deploy.sh` and run the script

```shell
cd twitter-data-pipeline
chmod +x ./sam-deploy.sh
./sam-deploy.sh
```

### streaming live tweets to kinesis firehose

run `tweet_collector.py` on your local machine and watch the tweets propagate through your piepline!