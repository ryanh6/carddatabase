from bs4 import BeautifulSoup
import requests

def readFullArts(galleryData):
    return galleryData.find_all("div", {"class": "wikia-gallery-item"})

def createGalleryLink(pageURL):
    cardName = pageURL.split("/")[-1]
    return "https://cardfight.fandom.com/wiki/Card_Gallery:" + cardName

def readPage(pageURL):
    pageRequest = requests.get(pageURL)
    return BeautifulSoup(pageRequest.text, "html.parser")

def editCardType(dictionary):
    if (dictionary.get("Card Type") == None):
        return ({"Card Type": "Normal Unit"})
    return ({"Grade": dictionary.get("Card Type")})

def editIllust(dictionary):
    if (dictionary.get("Illust") == None):
        return ({"Artist": dictionary.get("Design /  Illust")})
    else:
        return ({"Artist": dictionary.get("Illust")})

def editGrade(dictionary):
    if (dictionary.get("Grade / Skill") != None):
        splitGrade = dictionary.get("Grade / Skill").split(" / ")

        return ({"Grade": (splitGrade[0]).strip()})

    return ({"Grade": "-"})

def editSkill(dictionary):
    if (dictionary.get("Grade / Skill") != None):
        splitGrade = dictionary.get("Grade / Skill").split(" / ")

        if (len(splitGrade) > 1):
            return ({"Skill": (splitGrade[1]).strip()})

    return ({"Skill": "-"})

def editTrigger(dictionary):
    if (dictionary.get("Trigger Effect") != None):
        triggerEffect = dictionary.get("Trigger Effect").split(" / ")[0]
        return ({"Trigger Effect": triggerEffect})

    return ({"Trigger Effect": "-"})

def readCardEffect(pageData):
    try:
        cardEffect = pageData.find("table", {"class": "effect"})
        effectDescription = cardEffect.find("td")
        return ({"Card Effect(s)": (effectDescription.text).strip()})
    except:
        return ({"Card Effect(s)": "-"})

def readGiftMarker(pageData):
    print("hi")
    giftMarker = pageData.find_all()
    print(giftMarker)

def addAttributes(dictionary, attributes):
    for index in range(0, len(attributes)):
        if (index % 2 == 0):
            title = (attributes[index].text).strip()
            trait = (attributes[index + 1].text).strip()
            dictionary.update({title: trait})

    return dictionary

def deleteAttributes(dictionary):
    removeKeywords = ["Kanji", "Kana", "Phonetic", "Thai", "Italian", "Korean", "Grade / Skill", "Illust", "Design /  Illust", "Translation"]
    
    for key in removeKeywords:
        dictionary.pop(key, None)

    return dictionary

def createBasicDictionary(cardPageData, artworksArray):
    cardMainInfo = cardPageData.find("div", {"class": "info-main"})
    attributes = cardMainInfo.find_all("td")

    cardDictionary = {}
    addAttributes(cardDictionary, attributes)
    cardDictionary.update(readCardEffect(cardPageData))
    cardDictionary.update(readGiftMarker(cardMainInfo))
    cardDictionary.update(editCardType(cardDictionary))
    cardDictionary.update(editIllust(cardDictionary))
    cardDictionary.update(editGrade(cardDictionary))
    cardDictionary.update(editSkill(cardDictionary))
    cardDictionary.update(editTrigger(cardDictionary))
    deleteAttributes(cardDictionary)

    return cardDictionary

def cfvReadCard(pageURL):
    cardPageData = readPage(pageURL)
    galleryPageData = readPage(createGalleryLink(pageURL))

    artworksArray = readFullArts(galleryPageData)
    basicCard = createBasicDictionary(cardPageData, artworksArray)
    print(basicCard)

cfvReadCard("https://cardfight.fandom.com/wiki/King_of_Knights,_Alfred_(V_Series)")
