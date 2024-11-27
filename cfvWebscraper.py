from bs4 import BeautifulSoup
import requests

from database import *

def rebuildLink(oldLink):
    newString = ""
    splitString = oldLink.split("/")

    for section in splitString:
        if (section == "scale-to-width-down"):
            break
        else:
            newString += section + "/"
    
    return newString + "?" + oldLink.split("?")[-1]

def cfvCardArtworks(galleryData):
    imagesString = ""
    artworks = galleryData.find_all("div", {"class": "wikia-gallery-item"})
    # artworks += galleryData.find_all("div", string = "TD01/005EN (Sample)")

    # print(artworks)
    for element in artworks:
        print(element.text)
        print()

    # for element in artworks:
    #     next = element.previous_sibling
    #     image = next.find("img")
    #     finalImage = image.get("src")
    #     scaledImage = rebuildLink(finalImage)
    #     imagesString += scaledImage + ", "

    # if (imagesString == ""):
    #     return "-"
    
    # return imagesString[0:-2]

def findGiftMarker(targetClan):
    clanDictionary = {"Accel": ["Aqua Force", "Gold Paladin", "Great Nature", "Murakumo",
                                "Narukami", "Nova Grappler", "Pale Moon", "Tachikaze"],
                      "Force": ["Bermuda Triangle", "Dimension Police", "Gear Chronicle", "Genesis", "Kagero", 
                                "Link Joker", "Neo Nectar", "Royal Paladin", "Shadow Paladin", "Spike Brothers"],
                      "Protect": ["Angel Feathers", "Dark Irregulars", "Granblue",
                                  "Megacolony", "Nubatama", "Oracle Think Tank"]}
    
    for giftMarker in clanDictionary:
        for clan in clanDictionary[giftMarker]:
            if (clan == targetClan):
                return giftMarker

def addAttributes(dictionary):
    if (dictionary.get("Card Type") == None):
        dictionary.update({"Card Type": "Normal Unit"})

    if (dictionary.get("Illust") == None):
        dictionary.update({"Artist": dictionary.get("Design /  Illust")})
    else:
        dictionary.update({"Artist": dictionary.get("Illust")})

    return dictionary

def deleteAttributes(dictionary):
    toRemove = ["Kanji", "Kana", "Phonetic", "Thai", "Italian", "Korean", 
                "Grade / Skill", "Illust", "Design /  Illust", "Translation"]
    
    for key in toRemove:
        dictionary.pop(key, None)

    return dictionary

def editAttributes(dictionary):
    if (dictionary.get("Grade / Skill") != None):
        splitGrade = dictionary.get("Grade / Skill").split(" / ")

        dictionary.update({"Grade": (splitGrade[0]).strip()})
        if (len(splitGrade) > 1):
            dictionary.update({"Skill": (splitGrade[1]).strip()})

    if (dictionary.get("Imaginary Gift") != None):
        giftMarker = findGiftMarker(dictionary.get("Clan"))
        dictionary.update({"Imaginary Gift": giftMarker})

    if (dictionary.get("Trigger Effect") != None):
        triggerEffect = dictionary.get("Trigger Effect").split(" / ")[0]
        dictionary.update({"Trigger Effect": triggerEffect})

    return dictionary

def editDictionary(dictionary):
    dictionary = addAttributes(dictionary)
    dictionary = editAttributes(dictionary)
    dictionary = deleteAttributes(dictionary)
    return dictionary

def readCardEffect(pageData):
    try:
        cardEffect = pageData.find("table", {"class": "effect"})
        effectDescription = cardEffect.find("td")
        return ({"Card Effect(s)": (effectDescription.text).strip()})
    except:
        return ({"Card Effect(s)": "-"})

def readTournamentStatus(pageData, dictionary):
    language = dictionary.get("Language")

    try:
        status = pageData.find("table", {"class": "tourneystatus"})
        region = status.find("td", string = language)
        regulation = region.find_next("td")

        tourneyStatus = regulation.text.strip()

        if (tourneyStatus == "Unrestricted"):
            return ({"Restrictions": tourneyStatus})
        else:
            tourneyStatus = ((regulation.find("a")).get("title"))
            return ({"Restrictions": tourneyStatus})
    except:
        return

def readCardSets(pageData):
    try:
        cardSets = pageData.find("table", {"class": "sets"})
        setsDescription = (cardSets.find("td")).find_all("li")
    except:
        return
    
    codeList = []
    for set in setsDescription:
        codes = set.get_text(separator = " - ")

        splitedCodes = codes.split(" - ")
        splitedCodes = splitedCodes[2:]

        for code in splitedCodes:
            codeList.append(code)

    return codeList

# Need Edit: Full Art
# Second Edit: Card Art
# Outer Edit: Set Name, Release Date

def editSetAttributes(dictionary):
    code = dictionary.get("Card ID")

    dictionary.update({"Card ID": code.split(" ")[0]})
    dictionary.update({"Set ID": code.split("/")[0]})

    if (code[:2] == "V-"):
        dictionary.update({"Series": "V Series"})
        dictionary.update({"Format": "V-Premium"})
    elif (code[:2] == "D-" or code[:3] == "DZ-"):
        dictionary.update({"Series": "D Series"})
        dictionary.update({"Format": "Standard"})
    else:
        dictionary.update({"Series": "Original Series"})
        dictionary.update({"Format": "Premium"})

    if ("(" in code):
        rarity = code.split("(")[1].strip("()")
        dictionary.update({"Rarity": rarity})

    if ("EN" in code):
        dictionary.update({"Language": "EN"})
    elif ("KR" in code):
        dictionary.update({"Language": "KR"})
    elif ("TH" in code):
        dictionary.update({"Language": "TH"})
    elif ("IT" in code):
        dictionary.update({"Language": "IT"})
    else:
        dictionary.update({"Language": "JP"})


def cfvReadCard(pageURL):
    # Read Card Page (returns the Card Page Data,  error if doesnt exist)
    # Read Gallery Page (even if doesnt exists, its still fine)

    # Make the basic dictionary
    # Add card Effects
    # Add Full arts
    # Edit Attributes

    # Read Card sets
    # Make multiple dictionaries
    # Add tournament status
    # edit attributes (based on code provided)

    # Add To List

    try:
        cardRequest = requests.get(pageURL)
        cardPage = BeautifulSoup(cardRequest.text, "html.parser")

        cardMainInfo = cardPage.find("div", {"class": "info-main"})
        attributes = cardMainInfo.find_all("td")
    except:
        return
    
    cardList = []
    baseDictionary = {}
    for index in range(0, len(attributes)):
        if (index % 2 == 0):
            title = (attributes[index].text).strip()
            trait = (attributes[index + 1].text).strip()
            baseDictionary.update({title: trait})
    
    baseDictionary.update(readCardEffect(cardPage))
    editDictionary(baseDictionary)

    cardName = pageURL.split("/")[-1]
    cardGalleryLink = "https://cardfight.fandom.com/wiki/Card_Gallery:" + cardName

    try:
        galleryRequest = requests.get(cardGalleryLink)
        galleryPage = BeautifulSoup(galleryRequest.text, "html.parser")

        cfvCardArtworks(galleryPage)

        # baseDictionary.update(cfvCardArtworks(galleryPage, "Full Art"))
    except:
        # baseDictionary.update(({"Full Art(s)": "-"}))
        print("ERROR")

    codeArray = readCardSets(cardPage)
    # print(codeArray)

    for item in codeArray:
        newCard = baseDictionary.copy()
        newCard.update({"Card ID": item})
        editSetAttributes(newCard)
        newCard.update(readTournamentStatus(cardPage, newCard))
        cardList.append(newCard)


    # for card in cardList:
    #     print(card)

    # updateExcel("cfvdatabase.xlsx", "All Cards", cardList)

def readSet():
    # cfvReadCard("https://cardfight.fandom.com/wiki/King_of_Knights,_Alfred")
    cfvReadCard("https://cardfight.fandom.com/wiki/Blaster_Blade")
    # cfvReadCard("https://cardfight.fandom.com/wiki/Incandescent_Lion,_Blond_Ezel_(D_Series)")
    # cfvReadCard("https://cardfight.fandom.com/wiki/Epitome_of_Knowledge,_Silvest")

readSet()