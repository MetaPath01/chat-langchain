import os
import requests
import tweepy
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from getpass import getpass
from concurrent.futures import ThreadPoolExecutor, as_completed

# Enter your Twitter API credentials
consumer_key = getpass("Enter your consumer key: ")
consumer_secret = getpass("Enter your consumer secret: ")
def get_links(url):
    domain = urlparse(url).netloc

    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    urls = []
    for link in soup.find_all('a'):
        link_url = link.get('href')
        if link_url:
            link_domain = urlparse(link_url).netloc
            if not link_domain or link_domain == domain:
                urls.append(link_url)

    return urls

def get_twitter_api():
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api

def get_twitter_username_from_url(url):
    domain = urlparse(url).netloc
    if "twitter.com" in domain:
        return urlparse(url).path.split('/')[1]
    return None

def get_tweets(twitter_username, api, tweet_count=10):
    try:
        tweets = api.user_timeline(screen_name=twitter_username, count=tweet_count, tweet_mode='extended')
        return [tweet.full_text for tweet in tweets]
    except tweepy.TweepError as e:
        print(f"Error retrieving tweets for {twitter_username}: {e.reason}")
        return []

def save_tweets_to_file(username, tweets):
    folder = "twitter_data"
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(os.path.join(folder, f"{username}.txt"), 'w', encoding='utf-8') as f:
        for tweet in tweets:
            f.write(f"{tweet}\n\n")

def crawl_and_find_twitter_links(start_url):
    visited_urls = set()
    urls_to_visit = [start_url]
    twitter_links = []

    while urls_to_visit:
        current_url = urls_to_visit.pop()
        if current_url not in visited_urls:
            print(f"Visiting {current_url}")
            visited_urls.add(current_url)

            try:
                new_links = get_links(current_url)
                twitter_links.extend(link for link in new_links if "twitter.com" in urlparse(link).netloc)
                urls_to_visit.extend(link for link in new_links if link not in visited_urls)
            except Exception as e:
                print(f"Error processing {current_url}: {e}")

    return twitter_links

def process_link(current_url,twitter_api):
    print(f"Visiting {current_url}")

    try:
        new_links = get_links(current_url)
        twitter_links = [link for link in new_links if "twitter.com" in urlparse(link).netloc]

        for twitter_link in set(twitter_links):
            twitter_username = get_twitter_username_from_url(twitter_link)
            if twitter_username:
                tweets = get_tweets(twitter_username, twitter_api)
                if tweets:
                    save_tweets_to_file(twitter_username, tweets)
                    print(f"Saved tweets for {twitter_username}")

        return new_links

    except Exception as e:
        print(f"Error processing {current_url}: {e}")
        return []

def crawl_twitter_data(start_url, max_threads=10):
    twitter_api = get_twitter_api()

    visited_urls = set()
    urls_to_visit = [start_url]

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        while urls_to_visit:
            futures = {executor.submit(process_link, url,twitter_api): url for url in urls_to_visit}
            visited_urls |= set(urls_to_visit)  # Add new links to visited_urls

            urls_to_visit = []
            for future in as_completed(futures):
                new_links = future.result()
                urls_to_visit.extend(
                    link for link in new_links if link not in visited_urls
                )

if __name__ == "__main__":
    start_url = 'https://www.swft.pro/'
    crawl_twitter_data(start_url)