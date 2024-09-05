# Pip Installs Include...
# - pip install beautifulsoup4
# - pip install requests
# - pip install pandas
# - pip install lxml
# - pip install openpyxl

from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import requests

def fullImageLink(name):
    condensedName = name.replace(" ", "_")
    formattedName = condensedName.replace(",", "%2C")

    generatedLink = "https://cardfight.fandom.com/wiki/Card_Gallery:" + condensedName + "?file=" + formattedName + "_%28Full_Art%29.png"
    return generatedLink

def readCardInfo(pageURL):
    cardRequest = requests.get(pageURL)
    cardPage = BeautifulSoup(cardRequest.text, "html.parser")

    cardInformation = cardPage.find("div", {"class": "info-main"})
    cardTable = pd.read_html(StringIO(str(cardInformation)))[0]

    dictionary = {keyword: table.iloc[0, 1] for keyword, table in cardTable.groupby(0)}
    print(dictionary)

    print(dictionary.get("Name"))
    print(dictionary.get("Grade / Skill"))
    print(dictionary.get("Imaginary Gift"))
    print(dictionary.get("Power"))
    print(dictionary.get("Critical"))
    print(dictionary.get("Shield"))
    print(dictionary.get("Nation"))
    print(dictionary.get("Trigger Effect"))
    print(dictionary.get("Clan"))
    print(dictionary.get("Race"))
    print(dictionary.get("Illust"))

def readSetInfo(pageURL):
    setRequest = requests.get(pageURL)
    setPage = BeautifulSoup(setRequest.text, "html.parser")

    setList = setPage.find("table")
    setTable = pd.read_html(StringIO(str(setList)))[0]

    print(setTable.to_string())

readCardInfo("https://cardfight.fandom.com/wiki/Vampire_Princess_of_Night_Fog,_Nightrose_(V_Series)")
#readSetInfo("https://cardfight.fandom.com/wiki/Booster_Set_1:_Descent_of_the_King_of_Knights")