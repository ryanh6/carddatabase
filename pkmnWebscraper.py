from bs4 import BeautifulSoup
import requests

from database import *

# Base Website Used: https://pkmncards.com/sets/

def readPage(pageURL):
    pageRequest = requests.get(pageURL)
    return BeautifulSoup(pageRequest.text, "html.parser")

def readSet(pageURL):
    setPageData = readPage(pageURL)
    links = setPageData.find_all("article", {"class": "type-pkmn_card entry"})

    for element in links:
        cardLink = (element.find("a"))['href']
        print(cardLink)

def pkmnMain():
    columnNames = ["Name", "HP", "Type", "Class", 
                   "Stage", "Preevolutions", "Evolutions", "Attacks",
                   "Weakness", "Resistance", "Retreat",
                   "Illust", "Series", "Set", "Set Code", "Rarity", "Release Date",
                   "Regulations", "Format", "Text"]
    createExcel("pkmndatabase.xlsx", "All Cards", columnNames)

pkmnMain()

data = readSet("https://pkmncards.com/set/temporal-forces")