import requests

url = "https://www.nytimes.com/2023/03/22/us/politics/trump-lawyer-classified-documents-investigation.html"

response = requests.get(url)

print(response.content)