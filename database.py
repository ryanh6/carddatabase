import pandas as pd

def sortDatabase(dataframe, keyword):
    return dataframe.sort_values(keyword)
    # return dataframe.sort_values(["Release Date", "Card ID"])
    
def removeDuplicates(dataframe, keyword):
    return dataframe.drop_duplicates(keyword)

def formatDatabase(database):
    database = removeDuplicates(database, "Card ID")
    database = sortDatabase(database, "Card ID")
    return database

def createExcel(fileName, sheetName, columnNames):
    table = pd.DataFrame(columns = columnNames)
    table.to_excel(fileName, sheet_name = sheetName, index = False, na_rep = "-")

def updateExcel(fileName, sheetName, cardList):
    table = pd.read_excel(fileName)
    newRows = pd.DataFrame(cardList)

    combined = pd.concat([table, newRows])
    combined = formatDatabase(combined)

    with pd.ExcelWriter(fileName, mode = "a", engine = "openpyxl", if_sheet_exists = "replace") as writer:
        combined.to_excel(writer, sheet_name = sheetName, index = False, na_rep = "-")

def sortExcel(fileName, sheetName, keyword):
    table = pd.read_excel(fileName)

    print(table)
    sorted = sortDatabase(table, keyword)

    with pd.ExcelWriter(fileName, mode = "a", engine = "openpyxl") as writer:
        sorted.to_excel(writer, sheet_name = sheetName, index = False, na_rep = "-")