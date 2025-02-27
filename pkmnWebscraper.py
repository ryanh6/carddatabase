from bs4 import BeautifulSoup
import requests

# Base Website Used: https://pkmncards.com/sets/

def readPage(pageURL):
    pageRequest = requests.get(pageURL)
    return BeautifulSoup(pageRequest.text, "html.parser")

def decryptSymbol(pageContent):
    return pageContent.find("abbr", {"class": "ptcg-font ptcg-symbol-name"})

def retrieveName(pageContent):
    cardName = pageContent.find("span", {"title": "Name"})
    return ({"Name": cardName.text})

def retrieveHP(pageContent):
    cardHP = pageContent.find("span", {"title": "Hit Points"})
    
    if (cardHP != None):
        return ({"HP": cardHP.find("a").text})
    return ({"HP": "-"})

def retrieveElement(pageContent):
    section = pageContent.find("div", {"class": "name-hp-color"})
    cardElement = decryptSymbol(section)

    if (cardElement != None):
        return ({"Type": cardElement["title"]})
    return ({"Type": "-"})

def retrieveType(pageContent):
    cardType = pageContent.find("span", {"title": "Type"})
    return ({"Card Type": cardType.text})

def retrieveSubtype(pageContent):
    cardSubtype = pageContent.find("span", {"title": "Sub-Type"})
    
    if (cardSubtype != None):
        return ({"Card Type": cardSubtype.text})
    return ({"Subtype": "-"})

def retrieveStage(pageContent):
    cardStage = pageContent.find("span", {"title": "Stage of Evolution"})

    if (cardStage != None):
        return ({"Stage": cardStage.text})
    return ({"Stage": "-"})

def retrieveFlavorText(pageContent):
    cardFlavor = pageContent.find("div", {"class": "flavor minor-text"})
    return ({"Flavor Text": cardFlavor})

def retrieveImage(pageContent):
    cardImage = pageContent.find("a")
    return ({"Card Art": cardImage["href"]})

def readCardInfo(pageContent):
    cardDictionary = {}

    imageInfo = pageContent.find("div", {"class": "card-image-area"})
    textInfo = pageContent.find("div", {"class": "tab text"})


    cardDictionary.update(retrieveName(textInfo))
    # cardDictionary.update(retrieveHP(textInfo))
    # cardDictionary.update(retrieveElement(textInfo))
    # cardDictionary.update(retrieveType(textInfo))
    # cardDictionary.update(retrieveSubtype(textInfo))
    # cardDictionary.update(retrieveStage(textInfo))
    # cardDictionary.update(retrieveFlavorText(textInfo))
    cardDictionary.update(retrieveImage(imageInfo))
    print(cardDictionary)

def readSetInfo(pageURL):
    setPageData = readPage(pageURL)
    cards = setPageData.find_all("article", {"class": "type-pkmn_card entry"})

    for element in cards:
        cardInfo = (element.find("div", {"class": "entry-content"}))
        readCardInfo(cardInfo)

def allSets(pageURL):
    allSetsPageData = readPage(pageURL)
    section = allSetsPageData.find("div", {"class": "entry-content"})

    sets = section.find_all("li")

    for element in sets:
        mainLink = (element.find("a")["href"]) + "?sort=date&ord=auto&display=full"
        readSetInfo(mainLink)

# def pkmnMain():
#     columnNames = ["Card ID", "Name", "HP", "Type", "Class", 
#                    "Stage", "Preevolutions", "Evolutions", "Attacks",
#                    "Weakness", "Resistance", "Retreat",
#                    "Illust", "Series", "Set", "Set Code", "Rarity", "Release Date",
#                    "Regulations", "Format", "Text"]
#     createExcel("pkmndatabase.xlsx", "All Cards", columnNames)

# pkmnMain()

# data = readSetInfo("https://pkmncards.com/set/prismatic-evolutions/?sort=date&ord=auto&display=full")
allSets("https://pkmncards.com/sets/")