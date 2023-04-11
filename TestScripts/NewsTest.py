import requests
import datetime
from datetime import date

def format(article):
    replacements = {"“" : "\"", "”" : "\"", "’" : "'", "‘" : "'", "…": "..."}
    for k in replacements:
        article = article.replace(k, replacements[k])
    return article

def getUSHeadlines():
    today = date.today() - datetime.timedelta(3)
    descriptions = []

    sources = ["axios.com", "theguardian.com", "newsweek.com", "forbes.com", 
               "businessinsider.com", "usatoday.com", "npr.org", 
               "washingtonpost.com", "nbcnews.com"]
    
    for s in sources:
        params = {
                    "apiKey": "544e968c75464718852ae9cf280729af",
                    "language" : "en", #possible to search by source in params
                    "from" : str(today),
                    "domains" : s
                }
        url = " https://newsapi.org/v2/everything"

        response = requests.get(url = url, params = params).json()

        if response["status"] == "ok":
            descriptions.extend([format(article["description"]) for article in response["articles"]])

    return descriptions
    

if __name__ == "__main__":
    print(getUSHeadlines())