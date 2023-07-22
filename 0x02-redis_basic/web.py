#!/usr/bin/env python3

import requests
import time
import functools

# Decorator to handle caching and tracking access count
def cache_with_count(expiration_time=10):
    cache = {}

    def decorator(func):
        @functools.wraps(func)
        def wrapper(url):
            now = time.time()
            if url in cache and now - cache[url]['timestamp'] < expiration_time:
                cache[url]['count'] += 1
            else:
                response = func(url)
                cache[url] = {'response': response, 'timestamp': now, 'count': 1}
            return cache[url]['response']

        return wrapper

    return decorator

# Get the page content from a URL with caching and access count tracking
@cache_with_count()
def get_page(url: str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return ""

# Test the implementation with a slow response simulator
def main():
    slow_url = "http://slowwly.robertomurray.co.uk/delay/1000/url/https://www.example.com"
    fast_url = "https://www.example.com"

    print(get_page(slow_url))  # This will be slow due to the simulator
    print(get_page(slow_url))  # This should be cached and fast
    print(get_page(fast_url))  # This should be fetched again since it's a different URL
    print(get_page(fast_url))  # This should be cached and fast

if __name__ == "__main__":
    main()
