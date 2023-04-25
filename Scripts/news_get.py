'''
Name: 
news-get.py

Purpose:
Core script to extract keywords from news 
articles and transfer them to Firebase

Used by:
main.py
'''

import requests
import datetime
from datetime import date
import os
import random
from dotenv import load_dotenv

load_dotenv()

# Replaces some wonky unicode characters in 
# news articles to make parsing less awkward.
def format(article):
    replacements = {"“" : "\"", "”" : "\"", "’" : "'", "‘" : "'", "…": "..."}
    for k in replacements:
        article = article.replace(k, replacements[k])
    return article

# Makes an API request to NewsAPI's endpoint for
# articles from the past three days from a variety
# of reputable sources. 
def getUSHeadlines():
    today = date.today() - datetime.timedelta(3)
    descriptions = []

    sources = ["axios.com", "theguardian.com", "newsweek.com", "forbes.com", 
               "businessinsider.com", "usatoday.com",
               "washingtonpost.com", "nbcnews.com"]
    
    for s in sources:
        params = {
                    "apiKey": os.getenv("NEWSKEY"),
                    "language" : "en", #possible to search by source in params
                    "from" : str(today),
                    "domains" : s
                }
        url = " https://newsapi.org/v2/everything"

        response = requests.get(url = url, params = params).json()

        if response["status"] == "ok":
            descriptions.extend([format(article["description"]) for article in response["articles"]])

    return descriptions

def getRecentUsage(word):
    today = date.today() - datetime.timedelta(3)
    descriptions = []

    sources = ["axios.com", "theguardian.com", "newsweek.com", "forbes.com", 
               "businessinsider.com", "usatoday.com",
               "washingtonpost.com", "nbcnews.com"]
    
    params = {
            "apiKey": os.getenv("NEWSKEY"),
            "language" : "en", #possible to search by source in params
            "from" : str(today),
            "domains" : ','.join(sources),
            "q" : word
        }
    url = " https://newsapi.org/v2/everything"

    response = requests.get(url = url, params = params).json()

    if response["status"] == "ok":
        descriptions.extend([{"title": format(article["title"]), "source": article["source"]["name"], "url": article["url"]} for article in response["articles"]])

    return descriptions if len(descriptions) < 5 else descriptions[:5]
    

if __name__ == "__main__":
    print(getRecentUsage("draft"))