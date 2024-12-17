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

def readCardEffect(pageData):
    try:
        cardEffect = pageData.find("table", {"class": "effect"})
        effectDescription = cardEffect.find("td")
        return ({"Card Effect(s)": (effectDescription.text).strip()})
    except:
        return ({"Card Effect(s)": "-"})

def createBasicDictionary(cardPageData, artworksArray):
    cardMainInfo = cardPageData.find("div", {"class": "info-main"})
    attributes = cardMainInfo.find_all("td")

    cardDictionary = {}
    for index in range(0, len(attributes)):
        if (index % 2 == 0):
            title = (attributes[index].text).strip()
            trait = (attributes[index + 1].text).strip()
            cardDictionary.update({title: trait})

    cardDictionary.update(readCardEffect(cardPageData))

def cfvReadCard(pageURL):
    cardPageData = readPage(pageURL)
    galleryPageData = readPage(createGalleryLink(pageURL))

    artworksArray = readFullArts(galleryPageData)
    basicCard = createBasicDictionary(cardPageData, artworksArray)

cfvReadCard("https://cardfight.fandom.com/wiki/Blaster_Blade")
