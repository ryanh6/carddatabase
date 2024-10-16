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
    # cfvDataframe = arrangeColumns(cfvDataframe)
    cfvDataframe = removeDuplicates(cfvDataframe)
    cfvDataframe = sortDatabase(cfvDataframe)
    convertToExcel(cfvDataframe)

def convertToExcel(dataframe):
    dataframe.to_excel("cfvdatabase.xlsx", sheet_name = "All Cards", index = False, na_rep = '-')
