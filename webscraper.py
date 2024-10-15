from bs4 import BeautifulSoup
import requests
import re

# def findReleaseDate(set):
#     dateDictionary = {"BT01":"2011/02/26", "BT02":"", "BT03":"", "BT04":"", "BT05":"", "BT06":"", "BT07":"", "BT08":"",
#                       "BT09":"", "BT10":"", "BT11":"", "BT12":"", "BT13":"", "BT14":"", "BT15":"", "BT16":"", "BT17":"", 
#                       "G-BT01":"", "G-BT02":"", "G-BT03":"", "G-BT04":"", "G-BT05":"", "G-BT06":"", "G-BT07":"",
#                       "G-BT08":"", "G-BT09":"", "G-BT11":"", "G-BT11":"", "G-BT12":"", "G-BT13":"", "G-BT14":"", 
#                       "V-BT01":"", "V-BT02":"", "V-BT03":"", "V-BT04":"", "V-BT05":"", "V-BT06":"", 
#                       "V-BT07":"", "V-BT08":"", "V-BT09":"", "V-BT10":"", "V-BT11":"", "V-BT12":"", 
#                       "D-BT01":"", "D-BT02":"", "D-BT03":"", "D-BT04":"", "D-BT05":"", "D-BT06":"", "D-BT07":"",
#                       "D-BT08":"", "D-BT09":"", "D-BT10":"", "D-BT11":"", "D-BT12":"", "D-BT13":"",
#                       "DZ-BT01":"", "DZ-BT02":"", "DZ-BT03":"", "DZ-BT04":"", "DZ-BT05":"",
#                       "D-LBT01":"", "D-LBT02":"", "D-LBT03":"", "DZ-LBT01":"",}
    
#     return dateDictionary.get(set)

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
    # debutSet = dictionary.get("Card Set(s)").split(",")[0]
    # dictionary.update({"Card No.": debutSet})

    # releaseDate = findReleaseDate(debutSet)
    # dictionary.update({"Release Date": releaseDate})

    if (dictionary.get("Card Type") == None):
        dictionary.update({"Card Type": "Normal Unit"})

    if (dictionary.get("Illust") == None):
        dictionary.update({"Artist": dictionary.get("Design /  Illust")})
    else:
        dictionary.update({"Artist": dictionary.get("Illust")})

    return dictionary

def deleteAttributes(dictionary):
    toRemove = ["Kanji", "Kana", "Phonetic", "Thai", "Italian", "Korean", 
                "Grade / Skill", "Illust", "Design /  Illust"]
    
    for key in toRemove:
        dictionary.pop(key, None)

    return dictionary

def editAttributes(dictionary):
    # debutSet = dictionary.get("Card No.")

    # if (debutSet[0] == "V"):
    #     dictionary.update({"Format": "V Series"})
    # elif (debutSet[0] == "D"):
    #     dictionary.update({"Format": "D Series"})
    # else:
    #     dictionary.update({"Format": "Original Series"})

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

    dictionary = editDictionary(dictionary)

    #print(dictionary)

    return dictionary

cards = []
cards.append(readCard("https://cardfight.fandom.com/wiki/Blaster_Blade"))
cards.append(readCard("https://cardfight.fandom.com/wiki/Battleraizer"))
cards.append(readCard("https://cardfight.fandom.com/wiki/Cable_Sheep"))
cards.append(readCard("https://cardfight.fandom.com/wiki/Embodiment_of_Spear,_Tahr"))
cards.append(readCard("https://cardfight.fandom.com/wiki/Extreme_Battler,_Kenbeam"))
cards.append(readCard("https://cardfight.fandom.com/wiki/Dragonic_Overlord_(Break_Ride)"))
cards.append(readCard("https://cardfight.fandom.com/wiki/Flame_Wing_Steel_Beast,_Denial_Griffin"))
cards.append(readCard("https://cardfight.fandom.com/wiki/Incandescent_Lion,_Blond_Ezel_(V_Series)"))
cards.append(readCard("https://cardfight.fandom.com/wiki/Fated_One_of_Guiding_Star,_Welstra_%22Blitz_Arms%22"))
cards.append(readCard("https://cardfight.fandom.com/wiki/Destined_One_of_Scales,_Aelquilibra"))
cards.append(readCard("https://cardfight.fandom.com/wiki/Holy_Dragon,_Brave_Lancer_Dragon"))
cards.append(readCard("https://cardfight.fandom.com/wiki/Destruction_Tyrant,_Twintempest"))
cards.append(readCard("https://cardfight.fandom.com/wiki/Light_Source_Seeker,_Alfred_Exiv"))
print(cards)