from requests_html import HTMLSession

session = HTMLSession()

url = "https://www.cbsnews.com/news/syria-airstrike-us-contractor-killed-iran-drone-attack-joe-biden-lloyd-austin/"

response = session.get(url)

print(response.html.find("#site-content", first = True).text)