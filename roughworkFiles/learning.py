from bs4 import BeautifulSoup
import requests

with open("", "r") as file:
    document = BeautifulSoup(file, "html.praser")

print(document.prettify())

tag = document.title
print(tag.string)

moreTag = document.find_all("a")
print(moreTag)

anotherTag = document.find_all("a")[0]
print(anotherTag.find_all("p"))

#

url = ""

result = requests.get(url)
print(result.text)

secondDocument = BeautifulSoup(result.text, "html.parser")
print(secondDocument.prettify())

prices = secondDocument.find_all(text="$")
parent = prices[0].parent

print(parent)

strong = parent.find("strong")
print(strong.string)

