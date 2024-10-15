from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import time

def findReleaseDate(set):
    dateDictionary = {"BT01":"2011/03/12", "BT02":"2011/05/28", "BT03":"2011/08/06", "BT04":"2011/10/29", "BT05":"2012/01/14",
                      "BT06":"2012/04/28", "BT07":"2012/07/07", "BT08":"2012/09/22", "BT09":"2012/12/08",
                      "BT10":"2013/02/16", "BT21":"2013/04/27", "BT12":"2013/07/06", "BT13":"2011/09/13", "BT14":"2013/12/12", "BT15":"2014/02/28",
                      "BT16":"2014/05/16", "BT17":"2014/08/08",
                      "G-BT01":"2014/12/05", "G-BT02":"2015/02/20", "G-BT03":"2015/05/29", "G-BT04":"2015/08/28",
                      "G-BT05":"2015/11/13", "G-BT06":"2016/02/19", "G-BT07":"2016/05/27", "G-BT08":"2016/08/26",
                      "G-BT09":"2016/11/11", "G-BT10":"2017/02/03", "G-BT11":"2017/06/09", "G-BT12":"2017/08/25", 
                      "G-BT13":"2017/11/17", "G-BT14":"2018/02/23",
                      "V-BT01":"2018/05/25", "V-BT02":"2018/08/31", 
                      "V-BT03":"2018/12/14", "V-BT04":"2019/01/25", "V-BT05":"2019/07/12", "V-BT06":"2019/08/10",
                      "V-BT07":"2019/10/11", "V-BT08":"2020/06/19", 
                      "V-BT09":"2020/07/31", "V-BT10":"2020/08/28", "V-BT11":"2020/10/15", "V-BT12":"2020/11/06",
                      "D-BT01":"2021/04/17", "D-BT02":"2021/06/25", "D-BT03":"2021/09/24", "D-BT04":"2021/12/24", "D-BT05":"2022/04/01",
                      "D-BT06":"2022/08/05", "D-BT07":"2022/09/30", "D-BT08":"2022/12/09", 
                      "D-BT09":"2023/02/03", "D-BT10":"2023/04/07", "D-BT11":"2023/06/02", "D-BT12":"2023/08/04", "D-BT13":"2023/09/29",
                      "DZ-BT01":"2024/02/09", "DZ-BT03":"2024/06/07", "DZ-BT04":"2024/08/09", "DZ-BT05":"2024/10/11"}

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
    codesPattern = re.compile(r"(?:[A-Za-z]+-)?(?:BT|EB|TD|TCB|CHB|CB|CMB|MB|FC|SS|LD|SD|MBT)+(?:[0-9]+)?/[A-Za-z]*[0-9]+(?: |<br/>)")
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

    return dictionary

def main():
    startTime = time.time()

    list = []

    list.append(readCard("https://cardfight.fandom.com/wiki/Blaster_Blade"))
    list.append(readCard("https://cardfight.fandom.com/wiki/Battleraizer"))
    list.append(readCard("https://cardfight.fandom.com/wiki/Cable_Sheep"))
    list.append(readCard("https://cardfight.fandom.com/wiki/Embodiment_of_Spear,_Tahr"))
    list.append(readCard("https://cardfight.fandom.com/wiki/Extreme_Battler,_Kenbeam"))
    list.append(readCard("https://cardfight.fandom.com/wiki/Dragonic_Overlord_(Break_Ride)"))
    list.append(readCard("https://cardfight.fandom.com/wiki/Flame_Wing_Steel_Beast,_Denial_Griffin"))
    list.append(readCard("https://cardfight.fandom.com/wiki/Incandescent_Lion,_Blond_Ezel_(V_Series)"))
    list.append(readCard("https://cardfight.fandom.com/wiki/Fated_One_of_Guiding_Star,_Welstra_%22Blitz_Arms%22"))
    list.append(readCard("https://cardfight.fandom.com/wiki/Destined_One_of_Scales,_Aelquilibra"))
    list.append(readCard("https://cardfight.fandom.com/wiki/Holy_Dragon,_Brave_Lancer_Dragon"))
    list.append(readCard("https://cardfight.fandom.com/wiki/Destruction_Tyrant,_Twintempest"))
    list.append(readCard("https://cardfight.fandom.com/wiki/Light_Source_Seeker,_Alfred_Exiv"))

    print(list)

    # df = pd.DataFrame(list)
    # print(df)

    endTime = time.time()

    executionTime = endTime - startTime
    print(f"Execution time: {executionTime:.4f} seconds")

main()