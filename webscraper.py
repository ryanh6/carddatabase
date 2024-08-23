from bs4 import BeautifulSoup
import requests

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

def printArray(array):
    print("|", end = "")
    for item in array:
        print(" " + item + " |", end = "")
    print("")

def readCardInfo(pageURL):
    result = requests.get(pageURL)
    cardPage = BeautifulSoup(result.text, "html.parser")

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

    printArray(dataArray)





readCardInfo("https://cardfight.fandom.com/wiki/Battleraizer") 
readCardInfo("https://cardfight.fandom.com/wiki/Light_Element,_Agleam")
readCardInfo("https://cardfight.fandom.com/wiki/Hades_Hypnotist_(V_Series)")
readCardInfo("https://cardfight.fandom.com/wiki/Interdimensional_Beast,_Metallica_Phoenix_(V_Series)")
readCardInfo("https://cardfight.fandom.com/wiki/Vampire_Princess_of_Night_Fog,_Nightrose_(V_Series)")  
readCardInfo("https://cardfight.fandom.com/wiki/Extreme_Satellite_Weaponry,_Euryanthe")
readCardInfo("https://cardfight.fandom.com/wiki/Destined_One_of_Protection,_Alden")