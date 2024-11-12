from bs4 import BeautifulSoup
import requests

import openpyxl
import pandas as pd

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
                "Grade / Skill", "Illust", "Design /  Illust"]
    
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

    dictionary = editDictionary(dictionary)

    return dictionary

cardList = []
cardList.append(readCard("https://cardfight.fandom.com/wiki/Blaster_Blade"))
cardList.append(readCard("https://cardfight.fandom.com/wiki/Battleraizer"))
cardList.append(readCard("https://cardfight.fandom.com/wiki/Cable_Sheep"))
cardList.append(readCard("https://cardfight.fandom.com/wiki/Extreme_Battler,_Kenbeam"))
cardList.append(readCard("https://cardfight.fandom.com/wiki/Dragonic_Overlord_(Break_Ride)"))
cardList.append(readCard("https://cardfight.fandom.com/wiki/Flame_Wing_Steel_Beast,_Denial_Griffin"))
cardList.append(readCard("https://cardfight.fandom.com/wiki/Incandescent_Lion,_Blond_Ezel_(V_Series)"))
cardList.append(readCard("https://cardfight.fandom.com/wiki/Fated_One_of_Guiding_Star,_Welstra_%22Blitz_Arms%22"))

print(cardList)

table = pd.DataFrame(cardList)
table.to_excel("cfvdatabase.xlsx", sheet_name = "All Cards", index = False)