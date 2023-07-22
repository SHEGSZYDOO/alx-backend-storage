#!/usr/bin/env python3
"""
web cache and tracker
"""
import requests
import redis
from functools import wraps

store = redis.Redis()


def count_url_access(method):
    """ Decorator counting how many times
    a URL is accessed """
    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html = method(url)

        store.incr(count_key)
        store.set(cached_key, html)
        store.expire(cached_key, 10)
        return html
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """ Returns HTML content of a url """
    res = requests.get(url)
    return res.text
return ""

# Test the implementation with a slow response simulator
def main():
    slow_url = "http://slowwly.robertomurray.co.uk/delay/1000/url/https://www.example.com"
    fast_url = "https://www.example.com"

    print(get_page(slow_url))  # This will be slow due to the simulator
    print(get_page(slow_url))  # This should be cached and fast
    print(get_page(fast_url))  # This should be fetched again since it's a different URL
    print(get_page(fast_url))  # This should be cached and fast

    # Wait for more than 10 seconds to simulate cache expiration
    time.sleep(11)

    print(get_page(slow_url))  # This should be fetched again after expiration

if __name__ == "__main__":
    main()
