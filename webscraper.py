from bs4 import BeautifulSoup
import requests

def cleanText(givenString):
    givenString = givenString.strip()
    givenString = givenString.strip("\n")

    return givenString

def findTableSibling(tableItem):
    parent = tableItem.parent
    sibling = parent.find_next_sibling("td")
    item = cleanText(sibling.get_text())

    return item

def extractInfo(data, keyword):
    category = data.find(string = keyword)

    if (category != None):
        relevantData = findTableSibling(category)
    else:
        relevantData = "None"

    return relevantData
    

def readCardInfo(pageURL):
    result = requests.get(pageURL)
    cardPage = BeautifulSoup(result.text, "html.parser")

    infoString = "| "
    mainInfo = cardPage.find("div", {"class": "info-main"})

    infoString += extractInfo(mainInfo, "Name") + " | "
    infoString += extractInfo(mainInfo, "Card Type") + " | "
    infoString += extractInfo(mainInfo, "Imaginary Gift") + " | "
    infoString += extractInfo(mainInfo, "Special Icon") + " | "
    infoString += extractInfo(mainInfo, "Power") + " | "
    infoString += extractInfo(mainInfo, "Critical") + " | "
    infoString += extractInfo(mainInfo, "Shield") + " | "
    infoString += extractInfo(mainInfo, "Nation") + " | "
    infoString += extractInfo(mainInfo, "Clan") + " | "
    infoString += extractInfo(mainInfo, "Race") + " | "

    print(infoString)

readCardInfo("https://cardfight.fandom.com/wiki/Hades_Hypnotist_(V_Series)")  