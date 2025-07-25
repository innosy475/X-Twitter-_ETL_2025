import tweepy
import pandas as pd
from datetime import datetime



def run_twitter_etl():

    # Twitter authentication
    BEARER_TOKEN = "YOUR_BEARER_TOKEN"

    # Create API object
    client = tweepy.Client(bearer_token=BEARER_TOKEN)

    username = "username"
    user = client.get_user(username=username)
    user_id = user.data.id
    print(f"User ID for {username}: {user_id}")

    tweets_response = client.get_users_tweets(
        id=user_id,
        max_results=10,  # 5-100 tweets per request
        tweet_fields=["created_at", "public_metrics", "text", "conversation_id", "lang"]
    )

    # Extract tweets
    tweets_data = []
    if tweets_response.data:
        for tweet in tweets_response.data:
            tweets_data.append({
                "id": tweet.id,
                "created_at": tweet.created_at,
                "text": tweet.text,
                "retweets": tweet.public_metrics["retweet_count"],
                "likes": tweet.public_metrics["like_count"],
                "replies": tweet.public_metrics["reply_count"],
                "quotes": tweet.public_metrics["quote_count"],
                "language": tweet.lang
            })

    # Save to CSV

    if tweets_data:
        df = pd.DataFrame(tweets_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"s3://twitter-etl-bucket-airflow-docker/tweets_{username}_{timestamp}.csv"
        df.to_csv(output_file, index=False, encoding="utf-8")
        print(f"Saved {len(df)} tweets to {output_file}")
    else:
        print("No tweets found (maybe protected or no recent tweets).")