import tweepy
from kafka import KafkaProducer
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Twitter API credentials
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Kafka producer configuration
kafka_broker = "localhost:9092"
kafka_topic = "twitter_tweets"

# Authenticate with Twitter API using OAuth 2.0
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)

# Create a Kafka producer
producer = KafkaProducer(bootstrap_servers=[kafka_broker],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

class TwitterStreamListener(tweepy.Stream):
    def on_status(self, status):
        # Extract relevant information from the tweet
        tweet_data = {
            "text": status.text,
            "timestamp": str(status.created_at),
            "user": status.author.screen_name
        }
        
        # Send the tweet data to the Kafka topic
        producer.send(kafka_topic, tweet_data)
        print(f"Tweet sent to Kafka: {tweet_data}")
    
    def on_error(self, status_code):
        print(f"Error with status code: {status_code}")
        return True  # Don't kill the stream

# Create a Tweepy streaming client
stream_listener = TwitterStreamListener(consumer_key, consumer_secret,
                                        access_token, access_token_secret)

# Define the keywords or hashtags to track
keywords = ["banking EU", "EU banks", "European banking", "finance EU", "EU financial services",
            "#EUBanking", "#EuropeanBanks", "#EUFinance", "#EUFinancialServices"]

# Start the stream
stream_listener.filter(track=keywords)