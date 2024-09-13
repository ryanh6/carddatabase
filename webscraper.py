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
from openpyxl.utils import get_column_letter

def fullImageLink(name):
    condensedName = name.replace(" ", "_")
    formattedName = condensedName.replace(",", "%2C")

    generatedLink = "https://cardfight.fandom.com/wiki/Card_Gallery:" + condensedName + "?file=" + formattedName + "_%28Full_Art%29.png"
    return generatedLink

def formatDatabase():
    spreadsheet = openpyxl.load_workbook("cfvdatabase.xlsx")
    currentPage = spreadsheet.active

    for i in range(0, currentPage.max_column):
        maxLength = 0
        columnIndex = get_column_letter(i + 1)

        for j in range(0, currentPage.max_row):
            wordLength = len(str(currentPage.cell(row = j + 1, column = i + 1).value))

            if (wordLength > maxLength):
                maxLength = wordLength

        currentPage.column_dimensions[columnIndex].width = (maxLength + 5)

    spreadsheet.save("cfvdatabase.xlsx")

def clearDatabase():
    createDatabase()

def addHeaders(spreadsheet):
    currentPage = spreadsheet.active

    headers = ["Name", "Card Type", "Grade / Skill", "Imaginary Gift", 
               "Special Icon", "Trigger Effect", "Power", "Shield", 
               "Critical", "Nation", "Clan", "Race", "Format", "Illust", 
               "Design / Illust", "Card Set(s)", "Card Effect(s)"]
    
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

def retrieveCardInfo(pageURL):
    cardRequest = requests.get(pageURL)
    cardPage = BeautifulSoup(cardRequest.text, "html.parser")

    cardInformation = cardPage.find("div", {"class": "info-main"})
    cardTable = pd.read_html(StringIO(str(cardInformation)))[0]

    effectInformation = cardPage.find("table", {"class": "effect"})
    effectTable = pd.read_html(StringIO(str(effectInformation)))[0]

    print(effectTable)

    #cardTable = pd.concat([cardTable, effectTable])
    #print(cardTable)

    dictionary = {keyword: table.iloc[0, 1] for keyword, table in cardTable.groupby(0)}
    #print(dictionary)

    #writeCardInfo(dictionary)

def readSetInfo(pageURL):
    setRequest = requests.get(pageURL)
    setPage = BeautifulSoup(setRequest.text, "html.parser")

    setList = setPage.find("table")
    setTable = pd.read_html(StringIO(str(setList)))[0]

    print(setTable.to_string())

createDatabase()
retrieveCardInfo("https://cardfight.fandom.com/wiki/Battleraizer")
#retrieveCardInfo("https://cardfight.fandom.com/wiki/Vampire_Princess_of_Night_Fog,_Nightrose_(V_Series)")
#readSetInfo("https://cardfight.fandom.com/wiki/Booster_Set_1:_Descent_of_the_King_of_Knights")
#formatDatabase()