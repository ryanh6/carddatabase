from cfvWebscraper import *
from database import *

def cfvMain():
    columnNames = ["Card ID", "Name", "Card Type", "Grade", "Skill",
                    "Imaginary Gift", "Special Icon", "Trigger Effect",
                    "Power", "Shield", "Critical", "Nation", "Clan", "Race", 
                    "Series", "Format", "Artist", "Card Effect(s)", 
                    "Set ID", "Set Name", "Rarity", "Card Art(s)", "Release Date", 
                    "Language", "Restrictions", "Full Art(s)"]
    createExcel("cfvdatabase.xlsx", "All Cards", columnNames)

    readSet()

cfvMain()