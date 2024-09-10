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

def fullImageLink(name):
    condensedName = name.replace(" ", "_")
    formattedName = condensedName.replace(",", "%2C")

    generatedLink = "https://cardfight.fandom.com/wiki/Card_Gallery:" + condensedName + "?file=" + formattedName + "_%28Full_Art%29.png"
    return generatedLink

def verifyLink(pageURL):
    pageRequest = requests.get(pageURL)
    print(pageRequest.url)
    #page = BeautifulSoup(pageRequest.text, "html.parser")

    #allLinks = page.find("div", {"class": "info-main"})

def writeHeaders():
    database = openpyxl.load_workbook("cfvdatabase.xlsx")
    currentPage = database.active

    currentPage["A1"] = "Card No."
    currentPage["B1"] = "Name"
    currentPage["C1"] = "Card Type"
    currentPage["D1"] = "Grade / Skill"
    currentPage["E1"] = "Skill"
    currentPage["F1"] = "Imaginary Gift"
    currentPage["G1"] = "Special Icon"
    currentPage["H1"] = "Trigger Effect"
    currentPage["I1"] = "Power"
    currentPage["J1"] = "Shield"
    currentPage["K1"] = "Critical"
    currentPage["L1"] = "Nation"
    currentPage["M1"] = "Clan"
    currentPage["N1"] = "Race"
    currentPage["O1"] = "Illust"
    currentPage["P1"] = "Design / Illust"
    currentPage["Q1"] = "Format"
    currentPage["R1"] = "Rarity"

    database.save("cfvdatabase.xlsx")

def readCardInfo(pageURL):
    cardRequest = requests.get(pageURL)
    cardPage = BeautifulSoup(cardRequest.text, "html.parser")

    cardInformation = cardPage.find("div", {"class": "info-main"})
    cardTable = pd.read_html(StringIO(str(cardInformation)))[0]

    dictionary = {keyword: table.iloc[0, 1] for keyword, table in cardTable.groupby(0)}
    print(dictionary)

    #database = openpyxl.load_workbook("cfvdatabase.xlsx")
    #currentPage = database.active

    #headers = [currentPage.cell(row = 1, column = i).value for i in range(1, currentPage.max_column + 1)]
    
    #dataArray = []
    #for keyword in headers:
        #dataArray.append(str(dictionary.get(keyword)))
    
    #cardTuple = tuple(dataArray)
    #print(headers)
    #print(cardTuple)
    #currentPage.append(cardTuple)

    #database.save("cfvdatabase.xlsx")

def readSetInfo(pageURL):
    setRequest = requests.get(pageURL)
    setPage = BeautifulSoup(setRequest.text, "html.parser")

    setList = setPage.find("table")
    setTable = pd.read_html(StringIO(str(setList)))[0]

    print(setTable.to_string())

#readCardInfo("https://cardfight.fandom.com/wiki/Battleraizer")
#readCardInfo("https://cardfight.fandom.com/wiki/Vampire_Princess_of_Night_Fog,_Nightrose_(V_Series)")
#readSetInfo("https://cardfight.fandom.com/wiki/Booster_Set_1:_Descent_of_the_King_of_Knights")
#writeHeaders()

oldLink = fullImageLink("Destined One of Scales, Aelquilibra")
newLink = verifyLink(oldLink)