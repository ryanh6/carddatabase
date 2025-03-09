from bs4 import BeautifulSoup
import requests

# Base Website Used: https://pkmncards.com/sets/

# Helper Functions

def readPage(pageURL):
    pageRequest = requests.get(pageURL)
    return BeautifulSoup(pageRequest.text, "html.parser")

def decryptSymbol(pageContent):
    symbols = []
    typeList = pageContent.find_all("abbr", {"class": "ptcg-font ptcg-symbol-name"})

    for element in typeList:
        symbols.append(str(element["title"]).title())

    return symbols

def cleanText(rawText, symbols):
    counter = 0
    finalizedText = ""

    for character in range(len(rawText)):
        if (rawText[character] == "@"):
            continue
        if (rawText[character] == "*"):
            continue
        if (rawText[character] == "\n"):
            finalizedText += " - "
        elif (rawText[character - 1] == "{"):
            if (rawText[character] != "+"):
                finalizedText += symbols[counter]
                counter += 1

            character += 2
        else:
            finalizedText += rawText[character]

    return finalizedText

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

    if (len(cardElement) > 0):
        return ({"Type": cardElement[0]})
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

def retrievePreevolutions(pageContent):
    section = pageContent.find("span", {"class": "evolves"})

    if (section != None):
        cardPreEvolutions = section.find("a")

        if "from" in section.text:
            return ({"Preevolution": cardPreEvolutions.text})

    return ({"Preevolution": "-"})

def retrieveEvolutions(pageContent):
    evolutionList = []
    section = pageContent.find("span", {"class": "evolves"})

    if (section != None):
        cardEvolutions = section.find_all("a")
        
        for element in cardEvolutions:
            evolutionList.append(element.text)

        if "from" in section.text:
            evolutionList.pop(0)

        if (len(evolutionList) > 0):
            return ({"Evolutions": evolutionList})

    return ({"Evolutions": "-"})

def retrieveWeakness(pageContent):
    section = pageContent.find("span", {"title": "Weakness"})

    if (section == None):
        return ({"Weakness": "-"})
        
    cardWeakness = decryptSymbol(section)
    cardWeaknessModifier = section.find("span", {"title": "Weakness Modifier"})
    
    if (len(cardWeakness) == 0 or cardWeaknessModifier == None):
        return ({"Weakness": "-"})
    
    return ({"Weakness": str(cardWeakness[0]) + " " + str(cardWeaknessModifier.text)})

def retrieveResistance(pageContent):
    section = pageContent.find("span", {"title": "Resistance"})

    if (section == None):
        return ({"Resistance": "-"})
        
    cardResistance = decryptSymbol(section)
    cardResistanceModifier = section.find("span", {"title": "Resistance Modifier"})
    
    if (len(cardResistance) == 0 or cardResistanceModifier == None):
        return ({"Resistance": "-"})
    
    return ({"Resistance": str(cardResistance[0]) + " " + str(cardResistanceModifier.text)})

def retrieveRetreat(pageContent):
    cardRetreatCost = pageContent.find("span", {"title": "Retreat Cost"})

    if (cardRetreatCost != None):
        return ({"Retreat": (cardRetreatCost.text).split(" ")[1]})
    
    return ({"Retreat": "-"})

def retrieveMoves(pageContent):
    moveList = []
    section = pageContent.find("div", {"class": "text"})

    if (section != None):
        cardMoves = section.find_all("p")

        for element in cardMoves:
            symbols = decryptSymbol(element)
            rawText = element.text
            cardText = cleanText(rawText, symbols)
            moveList.append(str(cardText))

        return ({"Moves": moveList})

    return ({"Moves": "-"})

def retrieveArtist(pageContent):
    cardArtist = pageContent.find("a", {"title": "Illustrator"})

    if (cardArtist != None):
        return ({"Artist": cardArtist.text})
    
    return ({"Artist": "-"})

def retrieveSeries(pageContent):
    cardSeries = pageContent.find("span", {"title": "Series"})

    if (cardSeries != None):
        return ({"Series": cardSeries.text})
    
    return ({"Series": "Classic"})

def retrieveSet(pageContent):
    cardSet = pageContent.find("span", {"title": "Set"})
    return ({"Set": cardSet.text})

def retrieveSetCode(pageContent):
    cardSetCode = pageContent.find("span", {"title": "Set Series Code"})

    if (cardSetCode != None):
        return ({"Set": cardSetCode.text})
    
    return ({"Set": "-"})

def retrieveCardID(pageContent):
    IDString = ""
    cardSetCode = pageContent.find("span", {"title": "Set Abbreviation"})
    cardNumber = pageContent.find("a", {"title": "Number"})
    setTotal = pageContent.find("span", {"title": "Out Of"})

    if (cardSetCode != None):
        IDString += str(cardSetCode.text)
    if (cardNumber != None):
        IDString += " " + str(cardNumber.text)
    if (setTotal != None):
        IDString += str(setTotal.text)

    if (IDString != ""):
        return ({"Card ID": IDString})

    return ({"Card ID": "-"})

def retrieveRarity(pageContent):
    cardRarity = pageContent.find("a", {"title": "Rarity"})
    return ({"Rarity": cardRarity.text})

def retrieveReleaseDate(pageContent):
    cardReleaseDate = pageContent.find("span", {"title": "Date Released"})
    return ({"Release Date": (cardReleaseDate.text).split("↘ ")[1]})

def retrieveRulingText(pageContent):
    rulesList = []
    cardRules = pageContent.find("div", {"class": "rules minor-text"})

    if (cardRules != None):
        section = cardRules.find_all("div")
        for element in section:
            rulesString = str(element.text)[2:]
            rulesList.append(rulesString)

        return ({"Ruling Text": rulesList})
    return ({"Ruling Text": "-"})   

def retrieveFlavorText(pageContent):
    cardFlavor = pageContent.find("div", {"class": "flavor minor-text"})

    if (cardFlavor != None):
        flavorString = cleanText(cardFlavor.text, [])
        return ({"Flavor Text": flavorString})
    return ({"Flavor Text": "-"})

def retrieveMark(pageContent):
    cardMark = pageContent.find("span", {"class": "Regulation Mark"})

    if (cardMark != None):
        return ({"Mark": (cardMark.text).split(" ")[1]})
    
    return ({"Mark": "-"})

def retrieveFormats(pageContent):
    formatList = []
    formats = pageContent.find_all("span", {"title": "Format Type"})

    for element in formats:
        formatString = str(element.text)
        formatList.append(formatString)

    return ({"Formats": formatList})

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
    cardDictionary.update(retrievePreevolutions(textInfo))
    cardDictionary.update(retrieveEvolutions(textInfo))
    cardDictionary.update(retrieveWeakness(textInfo))
    cardDictionary.update(retrieveResistance(textInfo))
    cardDictionary.update(retrieveRetreat(textInfo))
    cardDictionary.update(retrieveMoves(textInfo))
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

# data = readSetInfo("https://pkmncards.com/set/prismatic-evolutions/?sort=date&ord=auto&display=full")
allSets("https://pkmncards.com/sets/")