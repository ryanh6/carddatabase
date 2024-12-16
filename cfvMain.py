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

    list = cfvReadCard("https://cardfight.fandom.com/wiki/Blaster_Blade")
    updateExcel("cfvdatabase.xlsx", "All Cards", list)
    sortExcel("cfvdatabase.xlsx", "Language Sorted", "Language")
    updateExcel("cfvdatabase.xlsx", "All Cards", list)
    sortExcel("cfvdatabase.xlsx", "Name Sorted", "Name")

    # readSet()

cfvMain()