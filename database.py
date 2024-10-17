import openpyxl
import pandas as pd

def arrangeColumns(dataframe):
    return dataframe[["Card No.", "Name", "Card Type", "Grade", "Skill", 
                      "Imaginary Gift", "Special Icon", "Trigger Effect", 
                      "Power", "Shield", "Critical", "Nation", "Clan", 
                      "Race", "Format", "Artist", "Full Art(s)", "Card Set(s)", 
                      "Rarity", "Card Effect(s)", "Release Date"]]

def sortDatabase(dataframe):
    return dataframe.sort_values(["Release Date", "Card No."])
    
def removeDuplicates(dataframe):
    return dataframe.drop_duplicates("Card No.")

def convertToPanda():
    return pd.read_excel("cfvdatabase.xlsx")

def filterDatabase(keyword):
    path = r"C:\Users\ryanh\Documents\Personal\Coding\carddatabase\cfvDatabase.xlsx"

    cfvDataframe = convertToPanda()
    values = (cfvDataframe[keyword].unique())
    values.sort()

    for word in values:
        filteredDataframe = cfvDataframe[cfvDataframe[keyword] == word]
        del filteredDataframe[keyword]

        with pd.ExcelWriter(path, mode = "a", engine = "openpyxl") as writer:
            filteredDataframe.to_excel(writer, sheet_name = word, index = False)

def formatDatabase():
    cfvDataframe = convertToPanda()
    print(cfvDataframe)
    # cfvDataframe = arrangeColumns(cfvDataframe)
    cfvDataframe = removeDuplicates(cfvDataframe)
    cfvDataframe = sortDatabase(cfvDataframe)
    # convertToExcel(cfvDataframe)
    cfvDataframe.to_excel("cfvdatabase.xlsx", sheet_name = "All Cards", index = False, na_rep = "-")

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

# def convertToExcel(dataframe):
#     path = r"C:\Users\ryanh\Documents\Personal\Coding\carddatabase\cfvDatabase.xlsx"

#     with pd.ExcelWriter(path, mode = "a", engine = "openpyxl", if_sheet_exists = "replace") as writer:
#         dataframe.to_excel(writer, sheet_name = "All Cards", index = False)