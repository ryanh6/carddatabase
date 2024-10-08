import openpyxl
import pandas as pd

def removeDuplicates():
    dataframe = pd.read_excel("cfvdatabase.xlsx")
    dataframeDuplicates = dataframe.drop_duplicates("Card No.")
    print(dataframeDuplicates.to_string())
    dataframeDuplicates.to_excel("cfvdatabase.xlsx", index = False)

# def formatDatabase(page):
#     removeDuplicates(page)

def addHeaders(page, excludeKey):
    headers = ["Card No.", "Name", "Card Type", "Grade", "Skill", "Imaginary Gift", "Special Icon", 
               "Trigger Effect", "Power", "Shield", "Critical", "Nation", "Clan", "Race", "Format", 
               "Artist", "Full Art(s)", "Card Set(s)", "Rarity", "Card Effect(s)"]

    index = 0
    for keyword in headers:
        if (keyword != excludeKey):
            page.cell(row = 1, column = index + 1).value = keyword
            index = index + 1

def createPage(spreadsheet, name, excludeKey):
    newPage = spreadsheet.create_sheet(name)
    addHeaders(newPage, excludeKey)

    return newPage

def createDatabase():
    spreadsheet = openpyxl.Workbook()
    currentPage = spreadsheet.active
    currentPage.title = "All Cards"

    addHeaders(currentPage, "")

    spreadsheet.save("cfvdatabase.xlsx")

def writeCardInfo(cardDictionary):
    spreadsheet = openpyxl.load_workbook("cfvdatabase.xlsx")
    currentPage = spreadsheet.active

    headers = []    
    for index in range(1, currentPage.max_column + 1):
        headers.append(currentPage.cell(row = 1, column = index).value)

    cardData = []
    for keyword in headers:
        if (cardDictionary.get(keyword) == None):
            cardData.append("-")
        else:
            cardData.append(str(cardDictionary.get(keyword)))
    
    currentPage.append(tuple(cardData))
    spreadsheet.save("cfvdatabase.xlsx")

# createDatabase()

spreadsheet = openpyxl.load_workbook("cfvdatabase.xlsx")
currentPage = spreadsheet.active
removeDuplicates()
