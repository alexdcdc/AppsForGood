import requests

def getUSHeadlines():
    params = {"apiKey": "544e968c75464718852ae9cf280729af",
            "country": "us"
            }
    url = " https://newsapi.org/v2/top-headlines"

    return requests.get(url = url, params = params)

