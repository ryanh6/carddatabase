from pkmnWebscraper import *
from database import *

def pkmnMain():
    columnNames = ["Name", "HP", "Type", "Class", 
                   "Stage", "Preevolutions", "Evolutions", "Attacks",
                   "Weakness", "Resistance", "Retreat",
                   "Illust", "Series", "Set", "Set Code", "Rarity", "Release Date",
                   "Regulations", "Format", "Text"]
    createExcel("pkmndatabase.xlsx", "All Cards", columnNames)

pkmnMain()