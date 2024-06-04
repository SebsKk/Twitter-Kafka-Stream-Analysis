from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from textblob import TextBlob
from SentimentVisualizer import SentimentVisualizer

# Initialize a SparkSession
spark = SparkSession.builder \
    .appName("TwitterSentimentAnalysis") \
    .getOrCreate()

# Define the schema for the tweet data
tweet_schema = StructType([
    StructField("text", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("user", StringType(), True)
])

# Create a Kafka consumer
kafka_topic = "twitter_tweets"
kafka_params = {
    "kafka.bootstrap.servers": "localhost:9092",
    "subscribe": kafka_topic,
    "startingOffsets": "earliest",
    "failOnDataLoss": "false"
}

# Read the tweet data from Kafka
tweets_df = spark \
    .readStream \
    .format("kafka") \
    .options(**kafka_params) \
    .load()

# Parse the JSON data from Kafka
parsed_tweets_df = tweets_df.select(from_json(col("value").cast("string"), tweet_schema).alias("tweet"))

processed_tweets_df = parsed_tweets_df.select("tweet.text", "tweet.timestamp", "tweet.user")

# Textblob sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity, analysis.sentiment.subjectivity

sentiment_udf = spark.udf.register("sentiment_analysis", analyze_sentiment, returnType="double")

sentiment_df = processed_tweets_df.withColumn("sentiment", sentiment_udf(col("text")))
sentiment_df = sentiment_df.select("text", "timestamp", "user", col("sentiment").getItem(0).alias("polarity"), col("sentiment").getItem(1).alias("subjectivity"))

query = sentiment_df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()


# Create an instance of the SentimentVisualizer
visualizer = SentimentVisualizer()

def process_batch(batch_df, batch_id):
    print(f"Processing batch: {batch_id}")
    for row in batch_df.collect():
        polarity = row.polarity
        subjectivity = row.subjectivity
        visualizer.add_data(polarity, subjectivity)

query = sentiment_df \
    .writeStream \
    .outputMode("append") \
    .foreachBatch(process_batch) \
    .start()

# Show the plot
visualizer.show_plot()

query.awaitTermination()
