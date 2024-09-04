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

    keyProperties = ["Name", "Card Type", "Grade / Skill", "Imaginary Gift",
                     "Special Icon", "Trigger Effect", "Power", "Critical",
                     "Shield", "Nation", "Clan", "Race"]
    
    cardInformation = cardPage.find("div", {"class": "info-main"})

def readSetInfo(pageURL):
    setRequest = requests.get(pageURL)
    setPage = BeautifulSoup(setRequest.text, "html.parser")

    setList = setPage.find("table")
    setTable = pd.read_html(StringIO(str(setList)))[0]

    print(setTable.to_string())

readSetInfo("https://cardfight.fandom.com/wiki/Booster_Set_1:_Descent_of_the_King_of_Knights")