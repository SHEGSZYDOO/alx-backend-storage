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

def main():
    slow_url = "http://slowwly.robertomurray.co.uk/delay/1000/url/https://www.example.com"
    fast_url = "https://www.example.com"

    print(get_page(slow_url))  
    print(get_page(slow_url))  
    print(get_page(fast_url))  
    print(get_page(fast_url))
    
    time.sleep(11)

    print(get_page(slow_url))

if __name__ == "__main__":
    main()
