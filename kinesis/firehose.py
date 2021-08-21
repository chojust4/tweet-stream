import logging
import boto3

FIREHOSE = "firehose"

class KinesisFirehose:

    def __init__(self, stream_name):
        self.stream_name = stream_name
        self.kinesis_client = boto3.client(FIREHOSE)

    def describe_delivery_stream(self):
        return self.kinesis_client.describe_delivery_stream(DeliveryStreamName=self.stream_name)

    def upload_raw_data(self, raw_data):
        logging.info("Starting to writing raw data to kinesis firehose ...")

        try:
            # encode data as bytes
            raw_data_encoded = raw_data.encode("utf-8")

            response = self.kinesis_client.put_record(
                DeliveryStreamName=self.stream_name,
                Record={
                    "Data": raw_data_encoded
                }
            )

            print(raw_data)

            logging.info("Successfully sent raw data, %s", response)

        except Exception as e:
            logging.error("Error writing data to firehose, %s", e)
            raise Exception(e)
