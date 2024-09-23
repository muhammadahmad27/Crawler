import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
import time
import json

def crawl(url, max_depth=2, delay=0.1):
    visited = set()
    
    def _crawl(url, depth):
        if depth > max_depth or url in visited:
            return
        visited.add(url)
        
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            print(f"Crawling: {url}")
            
            time.sleep(delay)
            
            links = []
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                full_url = urljoin(url, href)
                
                if full_url.startswith('http'):
                    links.append(full_url)
            
            with ThreadPoolExecutor() as executor:
                executor.map(lambda u: _crawl(u, depth + 1), links)
                
        except requests.RequestException as e:
            print(f"Failed to retrieve {url}: {e}")
    
    _crawl(url, 0)
    return visited

def save_to_json(data, filename='output.json'):
    with open(filename, 'w') as f:
        json.dump(list(data), f, indent=4)

# Start crawling from a given URL with delay and save to JSON
start_url = "https://www.nu.edu.pk/"
visited_urls = crawl(start_url, max_depth=2, delay=0.1)
save_to_json(visited_urls)
