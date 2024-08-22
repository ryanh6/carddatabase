from bs4 import BeautifulSoup
import requests

url = "https://cardfight.fandom.com/wiki/Booster_Set_1:_Descent_of_the_King_of_Knights"

result = requests.get(url)
#print(result.text)

wikiPage = BeautifulSoup(result.text, "html.parser")
#print(wikiPage.prettify())

table = wikiPage.find_all("table")[0]

rows = table.find_all("tr")

del rows[0]

for i in rows:
    code = i.find_all("td")[0]
    name = i.find_all("td")[1]
    print(code.string + " | " + name.string)

#print(rows.prettify())