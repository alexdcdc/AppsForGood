'''
Name:
news-get.py

Purpose:
Script to get recent news articles via NewsAPI

Used by:
main.py
'''

import requests
import datetime
from datetime import date
import os
import random
from dotenv import load_dotenv
from collections import Counter
import re

load_dotenv()

# Replaces some wonky unicode characters in
# news articles to make parsing less awkward. Also removes leftover HTML tags.


def format(article):
    replacements = {"“": "\"", "”": "\"", "’": "'", "‘": "'", "…": "..."}
    for k in replacements:
        article = article.replace(k, replacements[k])
    return re.sub("<[^>]{1,5}>", "", article)


# Makes an API request to NewsAPI's endpoint for
# articles from the past three days from a variety
# of reputable sources.
def getUSHeadlines():
    today = date.today() - datetime.timedelta(3)
    descriptions = []

    sources = ["theguardian.com", "newsweek.com", "forbes.com",
               "businessinsider.com", "usatoday.com",
               "washingtonpost.com", "nbcnews.com"]

    for s in sources:
        params = {
            "apiKey": os.getenv("NEWSKEY"),
            "language": "en",  # possible to search by source in params
            "from": str(today),
            "domains": s,
            "pageSize": 100
        }
        url = " https://newsapi.org/v2/everything"

        response = requests.get(url=url, params=params).json()

        if response["status"] == "ok":
            descriptions.extend([{"desc": format(article["description"]), "title": format(article["title"]), "source": article["source"]
                            ["name"], "url": article["url"]}
                                for article in response["articles"]])
        else:
            print("ERR: " + response["message"])

    return descriptions


#Gets recent news articles that utilize a given word.
def getRecentUsage(word):
    today = date.today() - datetime.timedelta(3)
    descriptions = []

    sources = ["axios.com", "theguardian.com", "newsweek.com", "forbes.com",
               "businessinsider.com", "usatoday.com",
               "washingtonpost.com", "nbcnews.com"]

    params = {
        "apiKey": os.getenv("NEWSKEY"),
        "language": "en",  # possible to search by source in params
        "from": str(today),
        "domains": ','.join(sources),
        "q": word
    }
    url = " https://newsapi.org/v2/everything"

    response = requests.get(url=url, params=params).json()

    if response["status"] == "ok":
        descriptions.extend([{"title": format(article["title"]), "source": article["source"]
                            ["name"], "url": article["url"]} for article in response["articles"]])
    else:
        print("ERR: " + response["message"])
        # descriptions.extend([article["source"]["name"] for article in response["articles"]])
    random.shuffle(descriptions)

    return descriptions if len(descriptions) < 5 else descriptions[:5]


#Gets count of news articles that utilize a given word.
def sourceCounts(word):
    today = date.today() - datetime.timedelta(3)
    descriptions = []

    sources = ["theguardian.com", "newsweek.com", "forbes.com",
               "businessinsider.com", "usatoday.com",
               "washingtonpost.com", "nbcnews.com"]

    for s in sources:
        params = {
            "apiKey": os.getenv("NEWSKEY"),
            "language": "en",  # possible to search by source in params
            "from": str(today),
            "domains": s,
            "pageSize": 50,
            "q": word
        }
        url = " https://newsapi.org/v2/everything"

        response = requests.get(url=url, params=params).json()

        if response["status"] == "ok":
            descriptions.extend([format(article["source"]["name"])
                                for article in response["articles"]])
        else:
            print("ERR: " + response["message"])

    return Counter(descriptions)


if __name__ == "__main__":
    words = getRecentUsage("carlson")
    print(words)