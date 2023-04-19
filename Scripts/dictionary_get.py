import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def getDefinitions(word):
    defs = []
    key = os.getenv("DICTKEY")
    url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + word + "?key=" + key

    response = requests.get(url)
    if (response.status_code != 200):
        print("Something went wrong while getting word definition")
        return
    for entry in response.json():
        if type(entry) != str:
            defs.extend(entry["shortdef"])

    return defs

def getSynonyms(word):
    key = os.getenv("THESKEY")
    url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + word + "?key=" + key

    response = requests.get(url)
    return response.json()


if __name__ == "__main__":
    print(getDefinitions("lead"))