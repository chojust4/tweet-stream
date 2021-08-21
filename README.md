### tweet-stream

`tweet-stream` is a simple, serverless data pipeline used to extract and transform live tweets in real time.  

The pipeline is built and deployed to AWS and backed by AWS cloudformation/SAM for provisioning cloud resources. 

![data-pipeline](https://github.com/chojust4/files/blob/main/aws-data-pipeline.png)

**TODO: setup connection to POST data to es domain from lambda**

---

### prerequisites

1. get api keys from the [twitter api](https://developer.twitter.com/en/docs) and specify credentials in `credentials.py`
2. download and configure the [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
3. install aws sam cli: 
```shell 
brew tap aws/tap
brew install aws-sam-cli
```
4. install python dependencies:
```shell
pip install -r requirements.txt
```

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

run `tweet_collector.py` on your local machine and watch the tweets propagate through your pipeline!
