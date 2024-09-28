from bs4 import BeautifulSoup
import requests

def readCard(pageURL):
    cardRequest = requests.get(pageURL)
    cardPage = BeautifulSoup(cardRequest.text, "html.parser")

    cardMainInfo = cardPage.find("div", {"class": "info-main"})
    attributes = cardMainInfo.find_all("td")

    print("(")
    for keywords in attributes:
        print((keywords.text).strip() + ", ")
    print(")")
    #print(cardMainInfo)

# Test Cases
readCard("https://cardfight.fandom.com/wiki/Blaster_Blade")
readCard("https://cardfight.fandom.com/wiki/Battleraizer")
readCard("https://cardfight.fandom.com/wiki/Cable_Sheep")
readCard("https://cardfight.fandom.com/wiki/Embodiment_of_Spear,_Tahr")
readCard("https://cardfight.fandom.com/wiki/Extreme_Battler,_Kenbeam")
readCard("https://cardfight.fandom.com/wiki/Dragonic_Overlord_(Break_Ride)")
readCard("https://cardfight.fandom.com/wiki/Flame_Wing_Steel_Beast,_Denial_Griffin")
readCard("https://cardfight.fandom.com/wiki/Incandescent_Lion,_Blond_Ezel_(V_Series)")
readCard("https://cardfight.fandom.com/wiki/Fated_One_of_Guiding_Star,_Welstra_%22Blitz_Arms%22")