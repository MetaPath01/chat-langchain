import tweepy
import csv
from dotenv import load_dotenv
import pathlib
import sys
import argparse
import os

if getattr(sys, 'frozen', False):
    script_location = pathlib.Path(sys.executable).parent.resolve()
else:
    script_location = pathlib.Path(__file__).parent.resolve()
load_dotenv(dotenv_path=script_location / '.env')

parser = argparse.ArgumentParser(description='Get Twitter data')
parser.add_argument('-u', '--userName',
                    help="Twitter's user name")
args = parser.parse_args()
userName = args.userName


def get_twitter_auth():
    auth = tweepy.OAuthHandler(
        os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_KEY_SECRET"))
    auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKE"),
                          os.getenv("TWITTER_ACCESS_SECRET"))
    return auth


def get_twitter_client():
    # auth = get_twitter_auth()
    print(os.getenv("TWITTER_BEARER_TOKEN"))
    print(os.getenv("TWITTER_API_KEY"))
    print(os.getenv("TWITTER_API_KEY_SECRET"))
    print(os.getenv("TWITTER_ACCESS_TOKEN"))
    print(os.getenv("TWITTER_ACCESS_SECRET"))
    client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
                           consumer_key=os.getenv("TWITTER_API_KEY"),
                           consumer_secret=os.getenv("TWITTER_API_KEY_SECRET"),
                           access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
                           access_token_secret=os.getenv(
                               "TWITTER_ACCESS_SECRET"),
                           wait_on_rate_limit=True)
    # client = tweepy.API(auth, wait_on_rate_limit=True)
    return client


def fetch_all_tweets(username):
    client = get_twitter_client()
    query = f"from:{username}"
    response = client.search_recent_tweets(
        query=query, max_results=100, expansions="author_id", tweet_fields=["created_at"])
    all_tweets = response.include_author_data(response.data)

    while response.next_token:
        response = client.search_recent_tweets(query=query, max_results=100, expansions="author_id", tweet_fields=[
                                            "created_at"], next_token=response.next_token)
        all_tweets.extend(response.include_author_data(response.data))

    return all_tweets


def save_tweets_to_csv(tweets, file_name="tweets.csv"):
    with open(file_name, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["User", "Tweet", "Time"])

        for tweet in tweets:
            writer.writerow(
                [tweet.user.screen_name, tweet.full_text, tweet.created_at])


if __name__ == "__main__":
    all_tweets = fetch_all_tweets(userName)
    save_tweets_to_csv(all_tweets, f"{userName}_tweets.csv")
