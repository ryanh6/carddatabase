from bs4 import BeautifulSoup
import pandas as pd
import requests

def readSetInfo(pageURL):
    setResult = requests.get(pageURL)
    setPage = BeautifulSoup(setResult.text, "html.parser")

    setInfo = setPage.find("table")
    print(setInfo)

    table = pd.read_html(setInfo)

readSetInfo("https://cardfight.fandom.com/wiki/Booster_Set_1:_Descent_of_the_King_of_Knights")