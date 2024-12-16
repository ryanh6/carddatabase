import pandas as pd
import openpyxl

def sortDatabase(dataframe):
    return dataframe.sort_values(["Release Date", "Card ID"])
    
def removeDuplicates(dataframe):
    return dataframe.drop_duplicates("Card ID")

def createExcel(fileName, sheetName, columnNames):
    table = pd.DataFrame(columns = columnNames)
    table.to_excel(fileName, sheet_name = sheetName, index = False, na_rep = "-")

def updateExcel(fileName, sheetName, cardList):
    table = pd.read_excel(fileName)
    newRows = pd.DataFrame(cardList)

    combined = pd.concat([table, newRows])
    combined.to_excel(fileName, sheet_name = sheetName, index = False, na_rep = "-")

# def formatDatabase(fileName, sheetName):
#     table = pd.read_excel(fileName)
#     table = removeDuplicates(table)
#     table = sortDatabase(table)
#     table.to_excel(fileName, sheet_name = sheetName, index = False, na_rep = "-")