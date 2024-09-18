# Pip Installs Include...
# - pip install beautifulsoup4
# - pip install requests
# - pip install pandas
# - pip install lxml
# - pip install openpyxl

from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import requests
import openpyxl
import re
from openpyxl.utils import get_column_letter

def rebuildLink(oldLink):
    newString = ""

    finalBit = oldLink.split("?")[-1]

    splitString = oldLink.split("/")
    for section in splitString:
        if (section == "scale-to-width-down"):
            break
        else:
            newString += section + "/"

    newString += "?" + finalBit

    return newString

def createImageLink(pageURL):
    images = ""

    cardName = pageURL.split("/")[-1]
    generatedLink = "https://cardfight.fandom.com/wiki/Card_Gallery:" + cardName

    pageRequest = requests.get(generatedLink)
    page = BeautifulSoup(pageRequest.text, "html.parser")

    imageLink = page.find_all("img", {"data-src": re.compile("_%28Full_Art(.*?)%29.png")})
    
    for image in imageLink:
        smallImage = image.get("data-src")
        fullImage = rebuildLink(smallImage)
        images += fullImage + ", "

    if (images == ""):
        return "No Full Arts"

    images = images[0:-2]
    return images

# def formatDatabase():
#     spreadsheet = openpyxl.load_workbook("cfvdatabase.xlsx")
#     currentPage = spreadsheet.active

#     for i in range(0, currentPage.max_column):
#         maxLength = 0
#         columnIndex = get_column_letter(i + 1)

#         for j in range(0, currentPage.max_row):
#             wordLength = len(str(currentPage.cell(row = j + 1, column = i + 1).value))

#             if (wordLength > maxLength):
#                 maxLength = wordLength

#         currentPage.column_dimensions[columnIndex].width = (maxLength + 5)

#     spreadsheet.save("cfvdatabase.xlsx")

def clearDatabase():
    createDatabase()

def addHeaders(spreadsheet):
    currentPage = spreadsheet.active

    headers = ["Name", "Card Type", "Grade / Skill", "Imaginary Gift", 
               "Special Icon", "Trigger Effect", "Power", "Shield", 
               "Critical", "Nation", "Clan", "Race", "Format", "Illust", 
               "Design / Illust", "Full Art Link(s)", "Card Set(s)", 
               "Card Effect(s)"]
    
    for i in range(0, len(headers)):
        currentPage.cell(row = 1, column = i + 1).value = headers[i]

def createDatabase():
    spreadsheet = openpyxl.Workbook()
    addHeaders(spreadsheet)

    spreadsheet.save("cfvdatabase.xlsx")

def writeCardInfo(dictionary):
    dataArray = []

    spreadsheet = openpyxl.load_workbook("cfvdatabase.xlsx")
    currentPage = spreadsheet.active

    headers = [currentPage.cell(row = 1, column = i).value for i in range(1, currentPage.max_column + 1)]

    for keyword in headers:
        dataArray.append(str(dictionary.get(keyword)))

    currentPage.append(tuple(dataArray))

    spreadsheet.save("cfvdatabase.xlsx")

def retrieveSpecialInfo(page, keyword):
    data = page.find("table", {"class": keyword})
    table = pd.read_html(StringIO(str(data)))[0]

    dictionary = table.to_dict('index')

    return dictionary[0]

def retrieveCardInfo(pageURL):
    cardRequest = requests.get(pageURL)
    cardPage = BeautifulSoup(cardRequest.text, "html.parser")

    cardInformation = cardPage.find("div", {"class": "info-main"})
    cardTable = pd.read_html(StringIO(str(cardInformation)))[0]

    effectInformation = retrieveSpecialInfo(cardPage, "effect")
    setInformation = retrieveSpecialInfo(cardPage, "sets")
    fullArts = createImageLink(pageURL)

    dictionary = {keyword: table.iloc[0, 1] for keyword, table in cardTable.groupby(0)}

    dictionary.update(effectInformation)
    dictionary.update(setInformation)
    dictionary.update({"Full Art Link(s)": fullArts})

    print(dictionary)

    writeCardInfo(dictionary)

# def readSetInfo(pageURL):
#     setRequest = requests.get(pageURL)
#     setPage = BeautifulSoup(setRequest.text, "html.parser")

#     setList = setPage.find("table")
#     setTable = pd.read_html(StringIO(str(setList)))[0]

#     print(setTable.to_string())

createDatabase()
retrieveCardInfo("https://cardfight.fandom.com/wiki/Battleraizer")
retrieveCardInfo("https://cardfight.fandom.com/wiki/Vampire_Princess_of_Night_Fog,_Nightrose_(V_Series)")
#readSetInfo("https://cardfight.fandom.com/wiki/Booster_Set_1:_Descent_of_the_King_of_Knights")

retrieveCardInfo("https://cardfight.fandom.com/wiki/Phantom_Blaster_Dragon_(Break_Ride)")
retrieveCardInfo("https://cardfight.fandom.com/wiki/Incandescent_Lion,_Blond_Ezel_(V_Series)")