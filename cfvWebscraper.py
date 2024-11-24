from bs4 import BeautifulSoup
import requests

# def cfvCardArtworks(cardGalleryLink):
#     galleryRequest = requests.get(cardGalleryLink)
#     galleryPage = BeautifulSoup(galleryRequest.text, "html.parser")

#     # artworks = galleryPage.find_all("div", {"class": "wikia-gallery-item"})
#     artworks = galleryPage.find_all("div", string = "Full Art")

#     for element in artworks:
#         # parent = element.parent
#         next = element.previous_sibling
#         image = next.find("img")
#         finalImage = image.get("src")
#         print(finalImage)
#         print()

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

def readCardSets(pageData):
    try:
        cardSets = pageData.find("table", {"class": "sets"})
        setsDescription = (cardSets.find("td")).find_all("li")

        print()
        for element in setsDescription:
            # print(element)

            # stringy = element
            # print("HI")
            # print(stringy)
            # print("WE")
            # # stringy = "Hello thereL"
            # new = stringy.replace("L", " - ")
            # print("YO")
            new = element.get_text(separator = " - ")
            print(new)
            # print("EH")
    except:
        return

def cfvReadCard(pageURL):
    try:
        cardRequest = requests.get(pageURL)
        cardPage = BeautifulSoup(cardRequest.text, "html.parser")

        cardMainInfo = cardPage.find("div", {"class": "info-main"})
        attributes = cardMainInfo.find_all("td")
    except:
        return
    
    dictionary = {}
    for index in range(0, len(attributes)):
        if (index % 2 == 0):
            title = (attributes[index].text).strip()
            trait = (attributes[index + 1].text).strip()
            dictionary.update({title: trait})
    
    dictionary.update(readCardEffect(cardPage))

    editDictionary(dictionary)

    print(dictionary)

    readCardSets(cardPage)

def readSet():
    cfvReadCard("https://cardfight.fandom.com/wiki/King_of_Knights,_Alfred")

readSet()
# cfvCardArtworks("https://cardfight.fandom.com/wiki/Card_Gallery:King_of_Knights,_Alfred")
# cfvCardArtworks("https://cardfight.fandom.com/wiki/Card_Gallery:Embodiment_of_Spear,_Tahr")