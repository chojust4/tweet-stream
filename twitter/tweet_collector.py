import credentials
import logging
from kinesis.firehose import KinesisFirehose
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

DELIVERY_STREAM_NAME = "TweetDeliveryStream"


class TwitterStreamer:
    # class for streaming live tweets

    def __init__(self):
        self.auth = self.authenticate()
        self.listener = TwitterStreamListener()

    def stream_tweets(self, hashtag_list):
        logging.info("Started streaming tweets for %s", hashtag_list)
        stream = Stream(self.auth, self.listener)
        stream.filter(track=hashtag_list)

    @staticmethod
    def authenticate():
        logging.info("Authenticating ...")
        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

        return auth


class TwitterStreamListener(StreamListener):
    # class for listening and writing tweets as json

    def __init__(self):
        super().__init__()
        self.kinesis_firehose = KinesisFirehose(DELIVERY_STREAM_NAME)

    def on_data(self, raw_data):
        logging.info("Started streaming live tweets ...")
        # load raw data into kinesis firehose
        self.kinesis_firehose.upload_raw_data(raw_data)

        return

    def on_error(self, status_code):
        # rate limiting
        if status_code == 420:
            return False


def main():
    # create instance of TwitterStreamer ~ will authenticate api keys
    streamer = TwitterStreamer()

    # configure list for filtering tweets here
    hashtag_list = ['badminton']
    streamer.stream_tweets(hashtag_list)


if __name__ == "__main__":
    main()
