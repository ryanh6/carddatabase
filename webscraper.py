import requests
from bs4 import BeautifulSoup
import pandas as pd

from io import StringIO
import re

import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
from openpyxl.styles import Alignment

def retrieveCardInfo(pageURL):
    cardRequest = requests.get(pageURL)
    cardPage = BeautifulSoup(cardRequest.text, "html.parser")

    try:
        # Extract the main table of card information on the page
        cardInformation = cardPage.find("div", {"class": "info-main"})
        cardTable = pd.read_html(StringIO(str(cardInformation)))[0]

        # Extract the special information, such as card effect, card sets and full art
        # effectInformation = retrieveSpecialInfo(cardPage, "effect")
        # setInformation = retrieveSpecialInfo(cardPage, "sets")
        # fullArts = createImageLink(pageURL)
    except:
        print("Not A Card Page")
        return

    # Create a dictionary for the card information
    dictionary = {keyword: table.iloc[0, 1] for keyword, table in cardTable.groupby(0)}

    # Add the special information to our dictionary
    # dictionary.update(effectInformation)
    # dictionary.update(setInformation)
    # dictionary.update({"Full Art Link(s)": fullArts})
    print(cardTable)

    print(dictionary)

    # editDictionary(dictionary)

    # Send dictionary to function to write into excel spreadsheet
    # writeCardInfo(dictionary)

retrieveCardInfo("https://cardfight.fandom.com/wiki/Extreme_Battler,_Kenbeam?so=search")