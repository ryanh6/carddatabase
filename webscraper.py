from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
from database import *

from io import StringIO

def makeCalender():
    dateDictionary = {}

    file = open("sets.txt", "r")

    for line in file:
        code = line.split(" - ")[0]
        date = line.split(" - ")[2]

        dateDictionary.update({code: date})

    return dateDictionary

def findReleaseDate(dictionary, set):
    code = set.split("/")[0]

    if (dictionary.get(code) == None):
        return "???"
    
    return dictionary.get(code).strip()

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
    debutSet = dictionary.get("Card Set(s)").split(",")[0]
    dictionary.update({"Card No.": debutSet})

    releaseDate = findReleaseDate(calender, debutSet)
    dictionary.update({"Release Date": releaseDate})

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
    debutSet = dictionary.get("Card No.")

    if (debutSet[0] == "V"):
        dictionary.update({"Format": "V Series"})
    elif (debutSet[0] == "D"):
        dictionary.update({"Format": "D Series"})
    else:
        dictionary.update({"Format": "Original Series"})

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

def rebuildLink(oldLink):
    newString = ""
    splitString = oldLink.split("/")

    for section in splitString:
        if (section == "scale-to-width-down"):
            break
        else:
            newString += section + "/"
    
    return newString + "?" + oldLink.split("?")[-1]

def cardFullArt(pageURL):
    cardName = pageURL.split("/")[-1]
    cardGalleryLink = "https://cardfight.fandom.com/wiki/Card_Gallery:" + cardName
    
    galleryRequest = requests.get(cardGalleryLink)
    galleryPage = BeautifulSoup(galleryRequest.text, "html.parser")

    regexPattern = re.compile("_%28Full_Art(.*?)%29.png")
    fullArts = galleryPage.find_all("img", {"data-src": regexPattern})

    imagesString = ""
    for images in fullArts:
        shrinkedImage = images.get("data-src")
        scaledImage = rebuildLink(shrinkedImage)
        imagesString += scaledImage + ", "
    
    if (imagesString == ""):
        return ({"Full Art(s)": "-"})
    
    return ({"Full Art(s)": imagesString[0:-2]})

def readCardRarities(page):
    cardSets = page.find("table", {"class": "sets"})
    setsDescription = (cardSets.find("td")).find_all("li")

    rarities = []
    rarityPattern = re.compile(r"\((.*?)\)")
    for set in setsDescription:
        rarities.extend(rarityPattern.findall(str(set)))

    raritiesString = ""
    for rarity in rarities:
        if (rarity not in raritiesString):
            raritiesString += rarity + " + "

    return ({"Rarity": raritiesString[0:-3]})

def readCardSets(page):
    cardSets = page.find("table", {"class": "sets"})
    setsDescription = (cardSets.find("td")).find_all("li")

    setCodes = []
    codesPattern = re.compile(r"(?:[A-Za-z]+-)?(?:BT|EB|TD|TCB|CHB|LBT|PR|CB|CMB|MB|FC|SS|LD|SD|MBT)+(?:[0-9]+)?/[A-Za-z]*[0-9]+(?: |<br/>)")
    for set in setsDescription:
        setCodes.extend(codesPattern.findall(str(set)))

    setString = ""
    for index in range(0, len(setCodes)):
        setString += (setCodes[index].split("<")[0]).strip() + ", "

    return ({"Card Set(s)": setString[0:-2]})

def readCardEffect(page):
    try:
        cardEffect = page.find("table", {"class": "effect"})
        effectDescription = cardEffect.find("td")
        return ({"Card Effect(s)": (effectDescription.text).strip()})
    except:
        return ({"Card Effect(s)": "-"})

def readCard(pageURL):
    try:
        cardRequest = requests.get(pageURL)
        cardPage = BeautifulSoup(cardRequest.text, "html.parser")

        cardMainInfo = cardPage.find("div", {"class": "info-main"})
        attributes = cardMainInfo.find_all("td")
    except:
        print("Not a Valid Card Page")
        return

    dictionary = {}
    for index in range(0, len(attributes)):
        if (index % 2 == 0):
            title = (attributes[index].text).strip()
            trait = (attributes[index + 1].text).strip()
            dictionary.update({title: trait})

    dictionary.update(readCardEffect(cardPage))
    dictionary.update(cardFullArt(pageURL))
    dictionary.update(readCardSets(cardPage))
    dictionary.update(readCardRarities(cardPage))

    dictionary = editDictionary(dictionary)

    writeCardInfo(dictionary)
    # return dictionary

def readSet(setURL):
    list = []

    setRequest = requests.get(setURL)
    setPage = BeautifulSoup(setRequest.text, "html.parser")

    setTable = setPage.find("table")
    rows = setTable.find_all("tr")
    rows = rows[1:]
    
    for links in rows:
        newLink = "https://cardfight.fandom.com" + links.find_all("td")[1].find("a").get("href")
        print(newLink)
        list.append(readCard(newLink))

    # return list

def main():
    readSet("https://cardfight.fandom.com/wiki/DZ_Booster_Set_01:_Fated_Clash")
    readSet("https://cardfight.fandom.com/wiki/DZ_Booster_Set_02:_Illusionless_Strife")
    # list.append(readSet("https://cardfight.fandom.com/wiki/DZ_Booster_Set_03:_Dimensional_Transcendence"))
    # list.append(readSet("https://cardfight.fandom.com/wiki/DZ_Booster_Set_04:_Destined_Showdown"))

    # table = pd.DataFrame(list)
    # convertToExcel(table)
    # formatDatabase()

calender = makeCalender()
main()
# formatDatabase()