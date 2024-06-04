# Twitter_Kafka_Stream_Analysis

## To run the project:

- run Zookeper
- run Kafka
- run Spark (standalone for the purpose of the project)
- create an appropriate Kafka Topic
- run TwitchStreamListener
- run sentiment_analysis

  # Description
This project demonstrates a real-time sentiment analysis pipeline for Twitter data using Apache Kafka, Apache Spark, and Python. The pipeline ingests tweets related to EU banking and finance, performs sentiment analysis using the TextBlob library, and visualizes the results in real-time using Matplotlib.

# Project Structure
The project consists of two main components:

- TwitchStreamListener.py: A Python script that uses the Tweepy library to connect to the Twitter API, filter tweets based on specified keywords, and publish the tweet data to a Kafka topic.
- sentiment_analysis.py: A Python script that sets up a Spark Streaming job to consume tweet data from the Kafka topic, perform sentiment analysis using TextBlob, and visualize the sentiment scores (polarity and subjectivity) in real-time using Matplotlib.
  
  # Tech stack

 
- Apache Kafka: 2.13-3.7.0
- Apache Spark: 2.12-3.5.1
- Apache Zookeeper: 3.8.4
- PySpark: 3.5.1
- kafka-python: 2.0.2
- textblob: 0.18.0.post0
- tweepy: 4.14.0
