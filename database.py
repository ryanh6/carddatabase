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

def cfvMain():
    columnNames = ["Card ID", "Name", "Card Type", "Grade", "Skill",
                    "Imaginary Gift", "Special Icon", "Trigger Effect",
                    "Power", "Shield", "Critical", "Nation", "Clan", "Race", 
                    "Series", "Format", "Artist", "Card Effect(s)", 
                    "Set ID", "Set Name", "Rarity", "Card Art(s)", "Release Date", 
                    "Language", "Restrictions", "Full Art(s)"]
    createExcel("cfvdatabase.xlsx", "All Cards", columnNames)

cfvMain()