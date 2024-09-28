from bs4 import BeautifulSoup
import requests
import re

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
                "Format", "Grade / Skill", "Illust", "Design /  Illust"]
    
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
        return ({"Full Art(s)": "None"})
    
    return ({"Full Art(s)": imagesString[0:-2]})

def readCardSets(page):
    cardSets = page.find("table", {"class": "sets"})
    setsDescription = (cardSets.find("td")).find_all("li")

    # codesPattern = re.compile("(?:[A-Za-z]+-)?[A-Za-z]+(?:[0-9]+)?/[A-Za-z]*[0-9]+(?![A-Za-z])")
    codesPattern = re.compile("(?:[A-Za-z]+-)?[A-Za-z]+(?:[0-9]+)?/[A-Za-z]*[0-9]+(?![A-Za-z]+)?")
    for set in setsDescription:
        print(set.text)
        setCodes = codesPattern.findall(str(set))
        print(setCodes)

def readCardEffect(page):
    try:
        cardEffect = page.find("table", {"class": "effect"})
        effectDescription = cardEffect.find("td")
        return ({"Card Effect(s)": (effectDescription.text).strip()})
    except:
        return ({"Card Effect(s)": "None"})

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

    readCardSets(cardPage)

    dictionary = editDictionary(dictionary)

    # for item in dictionary:
    #     print(item + ": " + dictionary.get(item))
    # print("")

# Test Cases
readCard("https://cardfight.fandom.com/wiki/Blaster_Blade")
readCard("https://cardfight.fandom.com/wiki/Battleraizer")
readCard("https://cardfight.fandom.com/wiki/Cable_Sheep")
readCard("https://cardfight.fandom.com/wiki/Embodiment_of_Spear,_Tahr")
readCard("https://cardfight.fandom.com/wiki/Extreme_Battler,_Kenbeam")
readCard("https://cardfight.fandom.com/wiki/Dragonic_Overlord_(Break_Ride)")
readCard("https://cardfight.fandom.com/wiki/Flame_Wing_Steel_Beast,_Denial_Griffin")
readCard("https://cardfight.fandom.com/wiki/Incandescent_Lion,_Blond_Ezel_(V_Series)")
readCard("https://cardfight.fandom.com/wiki/Fated_One_of_Guiding_Star,_Welstra_%22Blitz_Arms%22")
readCard("https://cardfight.fandom.com/wiki/Destined_One_of_Scales,_Aelquilibra")