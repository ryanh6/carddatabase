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
from openpyxl.styles import Font
from openpyxl.styles import Alignment

def removeDuplicates(array):
    newArray = []

    for item in array:
        if (item not in newArray):
            newArray.append(item)

    return newArray

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

def formatDatabase():
    spreadsheet = openpyxl.load_workbook("cfvdatabase.xlsx")
    currentPage = spreadsheet.active

    for i in range(0, currentPage.max_column):
        for j in range(0, currentPage.max_row):
            currentPage.cell(row = j + 1, column = i + 1).font = Font(size = 14)
    
        currentPage.cell(row = 1, column = i + 1).font = Font(bold = True, size = 16)

    for i in range(0, currentPage.max_column):
        maxLength = 0
        columnIndex = get_column_letter(i + 1)

        header = (currentPage.cell(row = 1, column = i + 1)).value

        if (header == "Full Art Link(s)" or header == "Card Effect(s)"):
            wordLength = len(str(header))
            currentPage.column_dimensions[columnIndex].width = (wordLength + 5)
            continue

        for j in range(0, currentPage.max_row):
            currentCell = currentPage.cell(row = j + 1, column = i + 1)

            wordLength = len(str(currentCell.value))

            if (wordLength > maxLength):
                maxLength = wordLength

            if (header == "Power" or header == "Shield" or header == "Critical"):
                currentCell.alignment = Alignment(horizontal='center')
            if (header == "Imaginary Gift" or header == "Special Icon" or header == "Trigger Effect"):
                currentCell.alignment = Alignment(horizontal='center')
            elif (currentCell.value == "-"):
                currentCell.alignment = Alignment(horizontal='center')

        currentPage.column_dimensions[columnIndex].width = (maxLength + 5)

    spreadsheet.save("cfvdatabase.xlsx")

# Clear the current excel spreadsheet
def clearDatabase():
    createDatabase()

# Add headers to the excel spreadsheet
def addHeaders(spreadsheet):
    currentPage = spreadsheet.active

    # List of all headers to be added
    headers = ["Card No.", "Name", "Card Type", "Grade", "Skill", 
               "Imaginary Gift", "Special Icon", "Trigger Effect", 
               "Power", "Shield", "Critical", "Nation", "Clan", 
               "Race", "Format", "Artist", "Full Art Link(s)", 
               "Card Set(s)", "Rarity", "Card Effect(s)"]
    
    # Add each header found in the array
    for i in range(0, len(headers)):
        currentPage.cell(row = 1, column = i + 1).value = headers[i]

# Creates a new excel spreadsheet
def createDatabase():
    # Open a new excel spreadsheet and assign headers
    spreadsheet = openpyxl.Workbook()
    addHeaders(spreadsheet)

    # Rename the current page of the spreadsheet
    currentPage = spreadsheet.active
    currentPage.title = "All Cards"

    spreadsheet.save("cfvdatabase.xlsx")

# def sortByHeader(sortKeyword):

def filterRarity(array):
    rarityString = ""
    rarityOrder = ['C', 'R', 'RR', 'RRR']

    # Find the Main Highest Rarity of the Card
    for rare in rarityOrder:
        for item in array:
            if (item == rare):
                rarityString = item

    # Find any other Rarities
    for item in array:
        toRemove = False
        for rare in rarityOrder:
            if (item == rare):
                toRemove = True
        
        # If we find Special Rarity, add to List
        if (toRemove == False):
            if (rarityString == ""):
                rarityString += item
            else:
                rarityString += "+" + item
    
    # Return our list of Rarities
    if (rarityString == ""):
        return "-"
    return rarityString

# Cleans the Data of the Dictionary before reading into Excel
def editDictionary(dictionary):
    # Each Clan has different Imaginary Gift, use that to assign Gift
    clanAccel = ["Aqua Force", "Gold Paladin", "Great Nature", "Murakumo",
                  "Narukami", "Nova Grappler", "Pale Moon", "Tachikaze"]
    clanForce = ["Bermuda Triangle", "Dimension Police", "Gear Chronicle",
                 "Genesis", "Kagero", "Link Joker", "Neo Nectar", 
                 "Royal Paladin", "Shadow Paladin", "Spike Brothers"]
    clanProtect = ["Angel Feathers", "Dark Irregulars", "Granblue",
                   "Megacolony", "Nubatama", "Oracle Think Tank"]

    # Any unspecified Card Types are Normal Units
    if (dictionary.get("Card Type") == None):
        dictionary.update({"Card Type": "Normal Unit"})

    # Split the Grade and Skill component into different sections
    gradeSkill = dictionary.get("Grade / Skill")
    splitGrade = gradeSkill.split("/")
    if (len(splitGrade) > 1):
        dictionary.update({"Grade": splitGrade[0].strip()})
        dictionary.update({"Skill": splitGrade[1].strip()})
    else:
        dictionary.update({"Grade": splitGrade[0].strip()})

    # Check for correct Imaginary Gift based on Clan
    if (dictionary.get("Imaginary Gift") != None):
        for clan in clanAccel:
            if (dictionary.get("Clan") == clan):
                dictionary.update({"Imaginary Gift": "Accel"})
        for clan in clanForce:
            if (dictionary.get("Clan") == clan):
                dictionary.update({"Imaginary Gift": "Force"})
        for clan in clanProtect:
            if (dictionary.get("Clan") == clan):
                dictionary.update({"Imaginary Gift": "Protect"})

    # Remove Power from Trigger Effect
    triggerEffect = dictionary.get("Trigger Effect")
    if (triggerEffect != None):
        splitTrigger = triggerEffect.split(" ")[0]
        dictionary.update({"Trigger Effect": splitTrigger})

    # Combine Illust and Design / Illust under Artist Keyword
    if (dictionary.get("Illust") == None):
        dictionary.update({"Artist": dictionary.get("Design / Illust")})
    else:
        dictionary.update({"Artist": dictionary.get("Illust")})

    # Regex to search all Codes of Card Sets
    allSets = dictionary.get("Card Set(s)")
    pattern = re.compile(r"(?:[A-Za-z]+-)?\b\w{2}\d{2}/[A-Za-z]*\d{2,3}\b(?![A-Za-z])|(?:[A-Za-z]+-)?\b\w{2}\d{2}/[A-Za-z]*S\d{2}\b(?![A-Za-z])")
    setCodes = pattern.findall(allSets)

    # First Code of Card Set is the Debut Set
    debutSet = setCodes[0]
    dictionary.update({"Card No.": debutSet})

    # Find the Card Series using the Debut Set
    if (debutSet[0] == "V"):
        dictionary.update({"Format": "V Series"})
    elif (debutSet[0] == "D"):
        dictionary.update({"Format": "D Series"})
    else:
        dictionary.update({"Format": "Original Series"})

    # Combine all Card Sets into a String
    cardSets = ""
    for code in setCodes:
        cardSets += code + ", "
    cardSets = cardSets[0:-2]

    dictionary.update({"Card Set(s)": cardSets})

    # Find all Rarities of a Card throughout Sets
    bracketPattern = re.compile(r"\((.*?)\)")
    rarities = bracketPattern.findall(allSets)
    rarities = removeDuplicates(rarities)

    # Filter out Irrelevant Rarities
    rarityString = filterRarity(rarities)

    dictionary.update({"Rarity": rarityString})

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
        if (dictionary.get(keyword) == None):
            dataArray.append("-")
        else:
            dataArray.append(str(dictionary.get(keyword)))

    # Once all information for the row is found, append row to excel spreadsheet
    currentPage.append(tuple(dataArray))

    spreadsheet.save("cfvdatabase.xlsx")

# Special function to retrieve information not found in main information table of a card page
def retrieveSpecialInfo(page, keyword):
    # Find a table based on a given keyword
    data = page.find("table", {"class": keyword})

    if (data == None):
        return ({"Card Effect(s)": "None"})

    table = pd.read_html(StringIO(str(data)))[0]

    # Create a mini dictionary based on the table
    dictionary = table.to_dict('index')

    return dictionary[0]

# Given the URL page of a card, retrieve information about the card
def retrieveCardInfo(pageURL):
    # Open the page for parsing given the URL
    cardRequest = requests.get(pageURL)
    cardPage = BeautifulSoup(cardRequest.text, "html.parser")

    categories = cardPage.find("div", {"class": "page-header__categories"})

    if (categories == None):
        return

    tag = categories.find(string = "Cards")

    if (tag == None):
        return

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

    editDictionary(dictionary)

    # Send dictionary to function to write into excel spreadsheet
    writeCardInfo(dictionary)

def retrieveSetInfo(pageURL):
    setRequest = requests.get(pageURL)
    setPage = BeautifulSoup(setRequest.text, "html.parser")

    setList = setPage.find("table")

    rowArray = setList.find_all("tr")
    rowArray = rowArray[1:]

    for row in rowArray:
        info = row.find_all("td")
        sourceLink = (info[1].find("a")).get("href")

        newLink = "https://cardfight.fandom.com" + sourceLink
        print(newLink)
        retrieveCardInfo(newLink)

# MAIN LOOP
# while (True):
#     command = ""

#     print("")
#     print("------------ List of Commands ------------")
#     print("CLEAR: Clears the Current Database")
#     print("READBYCARD: Read data of a card given a link")
#     print("READBYSET: Read data of a set given a link")
#     print("EXIT: Exit Program")
#     print("------------------------------------------")
#     command = (input("Enter a Command: ")).lower()
#     print("")

#     if (command == "clear"):
#         clearDatabase()
#     elif (command == "readbycard"):
#         link = input("Provide the URL of the Card: ")
#         retrieveCardInfo(link)
#     elif (command == "readbyset"):
#         link = input("Provide the URL of the Set: ")
#         retrieveSetInfo(link)
#     elif (command == "exit"):
#         break
#     else:
#         print("Not a Valid Command")

# TESTING
createDatabase()
retrieveCardInfo("https://cardfight.fandom.com/wiki/Destined_One_of_Exceedance,_Impauldio#English_")
retrieveCardInfo("https://cardfight.fandom.com/wiki/Vampire_Princess_of_Night_Fog,_Nightrose_(V_Series)")
retrieveCardInfo("https://cardfight.fandom.com/wiki/Battleraizer")
retrieveCardInfo("https://cardfight.fandom.com/wiki/Flame_Wing_Steel_Beast,_Denial_Griffin")
retrieveCardInfo("https://cardfight.fandom.com/wiki/Blaster_Blade?so=search")
retrieveCardInfo("https://cardfight.fandom.com/wiki/Crimson_Butterfly,_Brigitte")
formatDatabase()