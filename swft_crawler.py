import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def save_page(url, content):
    domain = urlparse(url).netloc
    path = os.path.join(domain, urlparse(url).path)
    folder = os.path.dirname(path)

    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(f"{domain}/{path}", 'w', encoding='utf-8') as f:
        f.write(content)

def process_url(current_url, visited_urls):
    print(f"Visiting {current_url}")

    try:
        response = requests.get(current_url)
        save_page(current_url, response.text)
        new_links = get_links(current_url)

        return new_links, visited_urls | {current_url}

    except Exception as e:
        print(f"Error processing {current_url}: {e}")
        return [], visited_urls

def crawl_website(start_url, max_threads=10):
    visited_urls = set()
    urls_to_visit = [start_url]

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        while urls_to_visit:
            futures = {executor.submit(process_url, url, visited_urls): url for url in urls_to_visit}

            urls_to_visit = []
            for future in as_completed(futures):
                new_links, visited = future.result()
                visited_urls |= visited  # union visited sets
                urls_to_visit.extend(link for link in new_links if link not in visited_urls)

    print("Crawl complete.")

if __name__ == "__main__":
    start_url = 'https://www.swft.pro/index.html'
    crawl_website(start_url)