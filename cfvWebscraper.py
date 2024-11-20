from bs4 import BeautifulSoup
import requests

def cfvCardArtworks(cardGalleryLink):
    galleryRequest = requests.get(cardGalleryLink)
    galleryPage = BeautifulSoup(galleryRequest.text, "html.parser")

    # sections = galleryPage.find("div", {"id": "gallery-0"})

    artworks = galleryPage.find_all("div", {"class": "wikia-gallery-item"})
    print(artworks)

    for element in artworks:
        # parent = element.parent
        # next = parent.previous_sibling
        image = element.find("img")
        finalImage = image.get("src")
        print(finalImage)
        print()

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
    
    print(dictionary)

cfvReadCard("https://cardfight.fandom.com/wiki/King_of_Knights,_Alfred")
cfvCardArtworks("https://cardfight.fandom.com/wiki/Card_Gallery:King_of_Knights,_Alfred")
cfvCardArtworks("https://cardfight.fandom.com/wiki/Card_Gallery:Embodiment_of_Spear,_Tahr")