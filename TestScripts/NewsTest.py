import requests

def removeSource(title):
    lastDash = 0
    for i in range(len(title)):
        if title[i] == "-":
            lastDash = i
    
    return title[:lastDash - 1]

def getUSHeadlines():
    params = {"apiKey": "544e968c75464718852ae9cf280729af",
            "country": "us", #possible to search by source in params
            "pageSize": 100
            }
    url = " https://newsapi.org/v2/top-headlines"

    response = requests.get(url = url, params = params).json()

    if response["status"] == "ok":
        return [removeSource(article["title"]) for article in response["articles"]]

    else:
        return None

    

if __name__ == "__main__":
    print(getUSHeadlines())