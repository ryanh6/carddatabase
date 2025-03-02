from bs4 import BeautifulSoup
import requests

# Base Website Used: https://pkmncards.com/sets/

# Helper Functions

def readPage(pageURL):
    pageRequest = requests.get(pageURL)
    return BeautifulSoup(pageRequest.text, "html.parser")

def decryptSymbol(pageContent):
    typeString = ""
    typeList = pageContent.find_all("abbr", {"class": "ptcg-font ptcg-symbol-name"})

    for element in typeList:
        typeString += str(element["title"]) + ", "

    return typeString[:-2]

# Retrieve Data Functions

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
        return ({"Type": cardElement})
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

def retrieveClass(pageContent):
    cardClass = pageContent.find("span", {"title": "Is"})

    if (cardClass != None):
        return ({"Class": cardClass.text[4:]})
    return ({"Class": "-"})

def retrieveWeakness(pageContent):
    section = pageContent.find("span", {"title": "Weakness"})

    if (section == None):
        return ({"Weakness": "-"})
        
    cardWeakness = decryptSymbol(section)
    cardWeaknessModifier = section.find("span", {"title": "Weakness Modifier"})
    
    if (cardWeakness == None or cardWeaknessModifier == None):
        return ({"Weakness": "-"})
    
    return ({"Weakness": str(cardWeakness) + " " + str(cardWeaknessModifier.text)})

def retrieveResistance(pageContent):
    section = pageContent.find("span", {"title": "Resistance"})

    if (section == None):
        return ({"Resistance": "-"})
        
    cardResistance = decryptSymbol(section)
    cardResistanceModifier = section.find("span", {"title": "Resistance Modifier"})
    
    if (cardResistance == None or cardResistanceModifier == None):
        return ({"Resistance": "-"})
    
    return ({"Resistance": str(cardResistance) + " " + str(cardResistanceModifier.text)})

def retrieveRetreat(pageContent):
    cardRetreatCost = pageContent.find("span", {"title": "Retreat Cost"})

    if (cardRetreatCost != None):
        return ({"Retreat": (cardRetreatCost.text).split(" ")[1]})
    
    return ({"Retreat": "-"})

def retrieveArtist(pageContent):
    cardArtist = pageContent.find("a", {"title": "Illustrator"})
    return ({"Artist": cardArtist.text})

def retrieveSeries(pageContent):
    cardSeries = pageContent.find("span", {"title": "Series"})
    return ({"Series": cardSeries.text})

def retrieveSet(pageContent):
    cardSet = pageContent.find("span", {"title": "Set"})
    return ({"Set": cardSet.text})

def retrieveSetCode(pageContent):
    cardSetCode = pageContent.find("span", {"title": "Set Series Code"})
    return ({"Set": cardSetCode.text})

def retrieveCardID(pageContent):
    cardSetCode = pageContent.find("span", {"title": "Set Abbreviation"})
    cardNumber = pageContent.find("a", {"title": "Number"})
    setTotal = pageContent.find("span", {"title": "Out Of"})
    return ({"Card ID": str(cardSetCode.text) + " " + str(cardNumber.text) + str(setTotal.text)})

def retrieveRarity(pageContent):
    cardRarity = pageContent.find("a", {"title": "Rarity"})
    return ({"Rarity": cardRarity.text})

def retrieveReleaseDate(pageContent):
    cardReleaseDate = pageContent.find("span", {"title": "Date Released"})
    return ({"Release Date": (cardReleaseDate.text)})

def retrieveRulingText(pageContent):
    rulesString = ""
    cardRules = pageContent.find("div", {"class": "rules minor-text"})

    if (cardRules != None):
        section = cardRules.find_all("div")
        for element in section:
            rulesString += str(element.text)[2:] + ", "

        return ({"Flavor Text": rulesString[:-2]})
    return ({"Flavor Text": "-"})   

def retrieveFlavorText(pageContent):
    cardFlavor = pageContent.find("div", {"class": "flavor minor-text"})

    if (cardFlavor != None):
        return ({"Flavor Text": cardFlavor.text})
    return ({"Flavor Text": "-"})

def retrieveMark(pageContent):
    cardMark = pageContent.find("span", {"class": "Regulation Mark"})
    return ({"Mark": (cardMark.text).split(" ")[1]})

def retrieveFormats(pageContent):
    formatString = ""
    formats = pageContent.find_all("span", {"title": "Format Type"})

    for element in formats:
        formatString += str(element.text) + ", "

    return ({"Formats": formatString[:-2]})

def retrieveImage(pageContent):
    cardImage = pageContent.find("a")
    return ({"Card Art": cardImage["href"]})

# Reading Overall Data Functions

def readCardInfo(pageContent):
    cardDictionary = {}

    imageInfo = pageContent.find("div", {"class": "card-image-area"})
    textInfo = pageContent.find("div", {"class": "tab text"})

    cardDictionary.update(retrieveName(textInfo))
    cardDictionary.update(retrieveHP(textInfo))
    cardDictionary.update(retrieveElement(textInfo))
    cardDictionary.update(retrieveType(textInfo))
    cardDictionary.update(retrieveSubtype(textInfo))
    cardDictionary.update(retrieveStage(textInfo))
    cardDictionary.update(retrieveClass(textInfo))
    # EVOLUTIONS (2 of them)
    cardDictionary.update(retrieveWeakness(textInfo))
    cardDictionary.update(retrieveResistance(textInfo))
    cardDictionary.update(retrieveRetreat(textInfo))
    # Moves
    cardDictionary.update(retrieveArtist(textInfo))
    cardDictionary.update(retrieveSeries(textInfo))
    cardDictionary.update(retrieveSet(textInfo))
    cardDictionary.update(retrieveSetCode(textInfo))
    cardDictionary.update(retrieveCardID(textInfo))
    cardDictionary.update(retrieveRarity(textInfo))
    cardDictionary.update(retrieveReleaseDate(textInfo))
    cardDictionary.update(retrieveRulingText(textInfo))
    cardDictionary.update(retrieveFlavorText(textInfo))
    cardDictionary.update(retrieveMark(textInfo))
    cardDictionary.update(retrieveFormats(textInfo))
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

data = readSetInfo("https://pkmncards.com/set/prismatic-evolutions/?sort=date&ord=auto&display=full")
# allSets("https://pkmncards.com/sets/")