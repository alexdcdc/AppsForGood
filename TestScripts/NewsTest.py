import requests

def removeSource(title):
    lastDash = 0
    for i in range(len(title)):
        if title[i] == "-":
            lastDash = i
    
    return title[:lastDash - 1]

def getUSHeadlines():
    params = {
                "apiKey": "544e968c75464718852ae9cf280729af",
                "language" : "en", #possible to search by source in params
                "from" : "2023-03-26",
                "domains" : "nbcnews.com"
            }
    url = " https://newsapi.org/v2/everything"

    response = requests.get(url = url, params = params).json()

    print(response)

    if response["status"] == "ok":
        return [article["description"] for article in response["articles"]]

    else:
        return None

    

if __name__ == "__main__":
    print(getUSHeadlines())