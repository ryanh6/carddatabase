import openpyxl
from webscraper import *

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

def createDatabase():
    spreadsheet = openpyxl.Workbook()
    currentPage = spreadsheet.active
    currentPage.title = "All Cards"

    addHeaders(currentPage, "")

    spreadsheet.save("cfvdatabase.xlsx")

createDatabase()