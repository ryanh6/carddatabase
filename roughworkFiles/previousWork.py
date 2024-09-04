from bs4 import BeautifulSoup
import requests

def buildImageLink(name):
    noSpace = name.replace(" ", "_")
    noCom = noSpace.replace(",", "%2C")

    link = "https://cardfight.fandom.com/wiki/Card_Gallery:" + noSpace + "?file=" + noCom + "_%28Full_Art%29.png"
    return link

def cleanText(givenString):
    givenString = givenString.split("/", 1)[0]
    givenString = givenString.strip()
    givenString = givenString.strip("\n")

    return givenString

def findTableSibling(tableItem):
    parent = tableItem.parent
    sibling = parent.find_next_sibling("td")
    item = cleanText(sibling.get_text())

    return item

def extractGradeSkill(data, array):
    category = data.find(string = "Grade / Skill")

    if (category != None):
        parent = category.parent
        relevantData = parent.find_next_sibling("td")

        attributes = relevantData.getText()
        attributes = attributes.split("/", 1)

        for item in attributes:
            item = item.strip()
            item = item.strip("\n")
            array.append(item)

        return
    else:
        relevantData = "None"
    
    array.append(relevantData)
    array.append(relevantData)

def extractGiftMarker(data):
    category = data.find(string = "Imaginary Gift")

    if (category != None):
        parent = category.parent
        relevantData = parent.find_next_sibling("td")
        
        marker = relevantData.find("a")
        relevantData = marker.get("title")
        relevantData = relevantData.split("/", 1)[1]
    else:
        relevantData = "None"
    
    return relevantData

def extractInfo(data, keyword):
    category = data.find(string = keyword)

    if (category != None):
        relevantData = findTableSibling(category)
    else:
        relevantData = "None"
    
    return relevantData

def readCardInfo(pageURL):
    cardResult = requests.get(pageURL)
    cardPage = BeautifulSoup(cardResult.text, "html.parser")

    dataArray = []
    keywords = ["Name", "Card Type", "Grade / Skill", "Imaginary Gift", "Special Icon",
                "Trigger Effect", "Power", "Critical", "Shield", "Nation", "Clan", "Race"]
    mainInfo = cardPage.find("div", {"class": "info-main"})

    for word in keywords:
        if (word == "Card Type"):
            cardType = extractInfo(mainInfo, word)

            if (cardType == "None"):
                dataArray.append("Normal Unit")
            else:
                dataArray.append(cardType)

        elif (word == "Grade / Skill"):
            extractGradeSkill(mainInfo, dataArray)

        elif (word == "Imaginary Gift"):
            dataArray.append(extractGiftMarker(mainInfo))

        else:
            dataArray.append(extractInfo(mainInfo, word))

    return dataArray

def readSetInfo(pageURL):
    setResult = requests.get(pageURL)
    setPage = BeautifulSoup(setResult.text, "html.parser")

    setInfo = setPage.find("table")
    cardList = setInfo.find_all("tr")

    headers = []

    count = 0
    for item in cardList[0].find_all("th"):
        headers.append(cleanText(item.text))
        count = count + 1

    del cardList[0]

    for card in cardList:
        cardData = []
        for title in headers:
            if (title == "Card No." or title == "Code"):
                cardCode = card.find_all("td")[0]
                cardCode = (cardCode.text).strip("\n")
                cardData.append(cardCode)

            elif (title == "Name"):
                if ("BT" in cardCode):
                    name = card.find_all("td")[1]
                elif ("TD" in cardCode):
                    name = card.find_all("td")[2]
                
                link = name.find("a")
                cardPageURL = "https://cardfight.fandom.com" + link.get("href")

                cardInfo = readCardInfo(cardPageURL)
                cardData.extend(cardInfo)

            elif (title == "Rarity"):
                cardRarity = card.find_all("td")[5]
                cardData.append(cardRarity.text)

        print(cardData)

readSetInfo("https://cardfight.fandom.com/wiki/Booster_Set_1:_Descent_of_the_King_of_Knights")
readSetInfo("https://cardfight.fandom.com/wiki/Trial_Deck_1:_Blaster_Blade")

#buildImageLink("Blaster Blade")