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

# Rebuilds the image link to remove shrinked size
def rebuildLink(oldLink):
    newString = ""

    # Grab contents of link after ?
    finalBit = oldLink.split("?")[-1]

    # Split string by /, rebuild until shrink properties
    splitString = oldLink.split("/")
    for section in splitString:
        # When we encounter shrink proporties, stop adding to string
        if (section == "scale-to-width-down"):
            break
        else:
            newString += section + "/"

    # Reattach the ending, return the new string
    newString += "?" + finalBit

    return newString

# Given the card page, create links to the full image of the card
def createImageLink(pageURL):
    # Array of images found
    images = ""

    # Retrieve name of card to access card gallery page
    cardName = pageURL.split("/")[-1]
    generatedLink = "https://cardfight.fandom.com/wiki/Card_Gallery:" + cardName

    pageRequest = requests.get(generatedLink)
    page = BeautifulSoup(pageRequest.text, "html.parser")

    # On gallery page, find all "full art" pictures on the page
    imageLink = page.find_all("img", {"data-src": re.compile("_%28Full_Art(.*?)%29.png")})
    
    # For each image found, grab the image link and reformat link
    for image in imageLink:
        smallImage = image.get("data-src")
        fullImage = rebuildLink(smallImage)
        images += fullImage + ", "

    if (images == ""):
        return "No Full Arts"

    # Remove ending comma and return list of full art images found
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

# Clear the current excel spreadsheet
def clearDatabase():
    createDatabase()

# Add headers to the excel spreadsheet
def addHeaders(spreadsheet):
    currentPage = spreadsheet.active

    # List of all headers to be added
    headers = ["Name", "Card Type", "Grade / Skill", "Imaginary Gift", 
               "Special Icon", "Trigger Effect", "Power", "Shield", 
               "Critical", "Nation", "Clan", "Race", "Format", "Illust", 
               "Design / Illust", "Full Art Link(s)", "Card Set(s)", 
               "Card Effect(s)"]
    
    # Add each header found in the array
    for i in range(0, len(headers)):
        currentPage.cell(row = 1, column = i + 1).value = headers[i]

# Creates a new excel spreadsheet
def createDatabase():
    # Open a new excel spreadsheet and assign headers
    spreadsheet = openpyxl.Workbook()
    addHeaders(spreadsheet)

    spreadsheet.save("cfvdatabase.xlsx")

# Given information about a card, write into the excel spreadsheet
def writeCardInfo(dictionary):
    # Array to track the contents of the row
    dataArray = []

    # Open the excel spreadsheet for writing
    spreadsheet = openpyxl.load_workbook("cfvdatabase.xlsx")
    currentPage = spreadsheet.active

    # Read the headers found in the excel spreadsheet already
    headers = [currentPage.cell(row = 1, column = i).value for i in range(1, currentPage.max_column + 1)]

    # For every header, find the corresponding information in the dictionary
    for keyword in headers:
        dataArray.append(str(dictionary.get(keyword)))

    # Once all information for the row is found, append row to excel spreadsheet
    currentPage.append(tuple(dataArray))

    spreadsheet.save("cfvdatabase.xlsx")

# Special function to retrieve information not found in main information table of a card page
def retrieveSpecialInfo(page, keyword):
    # Find a table based on a given keyword
    data = page.find("table", {"class": keyword})
    table = pd.read_html(StringIO(str(data)))[0]

    # Create a mini dictionary based on the table
    dictionary = table.to_dict('index')

    return dictionary[0]

# Given the URL page of a card, retrieve information about the card
def retrieveCardInfo(pageURL):
    # Open the page for parsing given the URL
    cardRequest = requests.get(pageURL)
    cardPage = BeautifulSoup(cardRequest.text, "html.parser")

    # Extract the main table of card information on the page
    cardInformation = cardPage.find("div", {"class": "info-main"})
    cardTable = pd.read_html(StringIO(str(cardInformation)))[0]

    # Extract the special information, such as card effect, card sets and full art
    effectInformation = retrieveSpecialInfo(cardPage, "effect")
    setInformation = retrieveSpecialInfo(cardPage, "sets")
    fullArts = createImageLink(pageURL)

    # Create a dictionary for the card information
    dictionary = {keyword: table.iloc[0, 1] for keyword, table in cardTable.groupby(0)}

    # Add the special information to our dictionary
    dictionary.update(effectInformation)
    dictionary.update(setInformation)
    dictionary.update({"Full Art Link(s)": fullArts})

    # Send dictionary to function to write into excel spreadsheet
    writeCardInfo(dictionary)

def readSetInfo(pageURL):
    setRequest = requests.get(pageURL)
    setPage = BeautifulSoup(setRequest.text, "html.parser")

    setList = setPage.find("table")
    #setTable = pd.read_html(StringIO(str(setList)))[0]

    links = setList.find_all("a")
    
    for thing in links:
        linkslinks = thing.get("href")
        print(linkslinks)

    #print(setTable.to_string())


# MY TESTS BEYOND HERE
createDatabase()
#retrieveCardInfo("https://cardfight.fandom.com/wiki/Battleraizer")
#retrieveCardInfo("https://cardfight.fandom.com/wiki/Vampire_Princess_of_Night_Fog,_Nightrose_(V_Series)")
readSetInfo("https://cardfight.fandom.com/wiki/Booster_Set_1:_Descent_of_the_King_of_Knights")

#retrieveCardInfo("https://cardfight.fandom.com/wiki/Phantom_Blaster_Dragon_(Break_Ride)")
#retrieveCardInfo("https://cardfight.fandom.com/wiki/Incandescent_Lion,_Blond_Ezel_(V_Series)")