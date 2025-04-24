from bs4 import BeautifulSoup
import requests
import math
import multiprocessing
import time

from database import *

# Base Website Used: https://scryfall.com/sets

# Helper Functions

def readPage(pageURL):
    pageRequest = requests.get(pageURL)
    return BeautifulSoup(pageRequest.text, "html.parser")

def decryptSymbol(pageContent):
    symbols = []
    typeList = pageContent.find_all("abbr")

    for element in typeList:
        symbols.append(str(element["title"]).title())
    
    return symbols

def cleanText(rawText, symbols):
    counter = 0
    finalizedText = ""

    for character in range(len(rawText)):
        if (rawText[character] == "\n"):
            finalizedText += " "
        elif (rawText[character - 1] == "{"):
            finalizedText += symbols[counter]
            character += 2
            counter += 1
        else:
            finalizedText += rawText[character]

    return finalizedText

# Retrieve Data Functions

def retrieveName(pageContent):
    cardName = pageContent.find("span", {"class": "card-text-card-name"})
    return ({"Name": (cardName.text).strip()})

def retrieveMana(pageContent):
    manaList = []
    cardMana = pageContent.find("span", {"class": "card-text-mana-cost"})

    if (cardMana != None):
        manaCost = decryptSymbol(cardMana)

        for element in manaCost:
            manaString = "{" + str(element) + "}"
            manaList.append(manaString)

        return ({"Mana": manaList})

    return ({"Mana": "-"})

def retrieveType(pageContent):
    cardType = pageContent.find("p", {"class": "card-text-type-line"})
    return ({"Type": (cardType.text).strip()})

def retrieveMoves(pageContent):
    moveList = []
    section = pageContent.find("div", {"class": "card-text-oracle"})

    if (section != None):
        cardMoves = section.find_all("p")

        for element in cardMoves:
            symbols = decryptSymbol(element)
            rawText = element.text
            cardText = cleanText(rawText, symbols)
            moveList.append(str(cardText))
        
        return ({"Moves": moveList})

    return ({"Moves": "-"})

def retrieveStats(pageContent):
    cardStats = pageContent.find("div", {"class": "card-text-stats"})
    
    if (cardStats != None):
        return ({"Stats": (cardStats.text).strip()})
    return ({"Stats": "-"})

def retrieveFlavor(pageContent):
    section = pageContent.find("div", {"class": "card-text-flavor"})

    if (section != None):
        cardFlavor = section.find("p")
        flavorString = cleanText((cardFlavor.text).strip(), [])

        return ({"Flavor Text": flavorString})
    return ({"Flavor Text": "-"})

def retrieveArtist(pageContent):
    section = pageContent.find("p", {"class": "card-text-artist"})

    if (section != None):
        cardArtist = section.find("a")
        return ({"Artist": cardArtist.text})
    
    return ({"Artist": "-"})

def retrieveFormats(pageContent):
    formatList = []
    formats = pageContent.find_all("div", {"class": "card-legality-item"})

    for element in formats:
        cardFormat = element.find("dt")
        cardLegality = element.find("dd")
        formatString = str(cardFormat.text) + ": " + str(cardLegality.text)
        formatList.append(formatString)

    return ({"Formats": formatList})

def retrieveSet(pageContent):
    cardSet = pageContent.find("span", {"class": "prints-current-set-name"})
    return ({"Set": ((cardSet.text).strip()).split(" ")[0]})

def retrieveSetCode(pageContent):
    setCode = pageContent.find("span", {"class": "prints-current-set-name"})
    return ({"Set Code": (((setCode.text).strip()).split(" ")[1])[1:-1]})

def retrieveCardID(pageContent):
    setCode = pageContent.find("span", {"class": "prints-current-set-name"})
    setID = (((setCode.text).strip()).split(" ")[1])[1:-1]

    cardNumber = pageContent.find("span", {"class": "prints-current-set-details"})
    return ({"Card ID": str(setID) + str(cardNumber.text.strip().split(" · ")[0])})

def retrieveRarity(pageContent):
    cardRarity = pageContent.find("span", {"class": "prints-current-set-details"})
    return ({"Rarity": cardRarity.text.strip().split(" · ")[1]})

def retrieveQuality(pageContent):
    cardQuality = pageContent.find("span", {"class": "prints-current-set-details"})
    return ({"Rarity": cardQuality.text.strip().split(" · ")[3]})

def retrieveImage(pageContent):
    section = pageContent.find("div", {"class": "card-image-front"})
    cardImage = section.find("img")
    return ({"Card Art": cardImage["src"]})

# Reading Overall Data Functions

def readCardInfo(pageContent):
    cardDictionary = {}

    imageInfo = pageContent.find("div", {"class": "card-image"})
    textInfo = pageContent.find("div", {"class": "card-text"})
    printInfo = pageContent.find("div", {"class": "prints"})

    cardDictionary.update(retrieveName(textInfo))
    cardDictionary.update(retrieveMana(textInfo))
    cardDictionary.update(retrieveType(textInfo))
    cardDictionary.update(retrieveMoves(textInfo))
    cardDictionary.update(retrieveStats(textInfo))
    cardDictionary.update(retrieveFlavor(textInfo))
    cardDictionary.update(retrieveArtist(textInfo))
    cardDictionary.update(retrieveFormats(textInfo))
    cardDictionary.update(retrieveSet(printInfo))
    cardDictionary.update(retrieveSetCode(printInfo))
    cardDictionary.update(retrieveCardID(printInfo))
    cardDictionary.update(retrieveRarity(printInfo))
    cardDictionary.update(retrieveQuality(printInfo))
    cardDictionary.update(retrieveImage(imageInfo))
   
    return cardDictionary

def readSetInfo(pageURL):
    cardList = []
    setPageData = readPage(pageURL)
    cards = setPageData.find_all("div", {"class": "card-profile"})

    for element in cards:
        cardInfo = (element.find("div", {"class": "inner-flex"}))
        cardList.append(readCardInfo(cardInfo))

    return cardList

def allSets(pageURL):
    links = []
    fullList = []
    allSetsPageData = readPage(pageURL)
    table = allSetsPageData.find("table", {"class": "checklist"})
    tableBody = table.find("tbody")

    row = tableBody.find_all("tr")

    for element in row:
        cardSet = (element.find("a")["href"]).split("/")[-1]
        cardNumber = (element.find("a", {"tabindex": -1})).text
        pages = math.ceil(int(cardNumber) / 20)

        for index in range(pages):
            mainLink = "https://scryfall.com/search?as=full&order=set&page=" + str(index) + "&q=set%3A" + cardSet + "&unique=prints"
            links.append(mainLink)

    with multiprocessing.Pool() as pool:
        results = pool.map(readSetInfo, links)
        pool.close()
        pool.join()

    for dictionary in results:
        fullList.extend(dictionary)

    table = (dictionaryToDataframe(fullList))
    updateFile(table, 'mtgdatabase.xlsx')

# data = readSetInfo("https://scryfall.com/search?as=full&order=name&page=18&q=set%3Ada1&unique=prints")
# data = readSetInfo("https://scryfall.com/search?as=full&order=name&q=set%3Atdm&unique=prints")
# table = (dictionaryToDataframe(data))
# updateFile(table, 'mtgdatabase.xlsx')
# allSets("https://scryfall.com/sets")

# if __name__ == '__main__':
#     multiprocessing.freeze_support()
#     startTime = time.time()
#     allSets("https://scryfall.com/sets")
#     endTime = time.time()

#     elapsedTime = endTime - startTime
#     print(f"Elapsed time: {elapsedTime:.4f} seconds")