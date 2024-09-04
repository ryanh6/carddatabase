from bs4 import BeautifulSoup
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
