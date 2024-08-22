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
    link = name.find("a")
    #print("https://cardfight.fandom.com" + link.get("href"))
    print(code.string + " | " + name.string + " | ", end='')

    subUrl = "https://cardfight.fandom.com" + link.get("href")
    subResult = requests.get(subUrl)
    cardPage = BeautifulSoup(subResult.text, "html.parser")

    infoString = ""
    info = cardPage.find("div", {"class": "info-main"})
    #print(info)

    type = info.find(string="Card Type")
    #Found the Clan row, tooks its parent's parent's child (aka sibling), found the a link, then the string associated with the a link
    if (type != None):    
        typeInfo = (((type.parent).parent).find_all("td")[1]).find("a")
        infoString += typeInfo.string + " | "
    else:
        infoString += "Normal Unit" + " | "

    clan = info.find(string="Clan")
    #Found the Clan row, tooks its parent's parent's child (aka sibling), found the a link, then the string associated with the a link
    clanInfo = (((clan.parent).parent).find_all("td")[1]).find("a")
    infoString += clanInfo.string + " | "

    race = info.find(string="Race")
    #Found the Clan row, tooks its parent's parent's child (aka sibling), found the a link, then the string associated with the a link
    raceInfo = (((race.parent).parent).find_all("td")[1]).find("a")
    infoString += raceInfo.string + " | "

    print(infoString)

#print(rows.prettify())