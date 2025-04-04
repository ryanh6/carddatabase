# from bs4 import BeautifulSoup
# import requests

# import pandas as pd
# from database import *

# def readFullArts(galleryData):
#     return galleryData.find_all("div", {"class": "wikia-gallery-item"})

# def createGalleryLink(pageURL):
#     cardName = pageURL.split("/")[-1]
#     return "https://cardfight.fandom.com/wiki/Card_Gallery:" + cardName

# def rescaleImage(image):
#     newString = ""
#     splitString = image.split("/")

#     for section in splitString:
#         if (section == "scale-to-width-down"):
#             break
#         else:
#             newString += section + "/"
    
#     return newString + "?" + image.split("?")[-1]

# def searchArtworks(artworks, keyword):
#     imagesString = ""

#     for element in artworks:
#         if (keyword in element.text and "IT" not in element.text):
#             try:
#                 image = element.find("img")
#                 imageSource = image.get("src")
#                 scaledImage = rescaleImage(imageSource)
                
#                 imagesString += scaledImage + ", "
#             except:
#                 continue

#     if (imagesString == ""):
#         return ({"Full Art(s)": "-"})
    
#     return ({"Full Art(s)": imagesString[0:-2]})

# def readPage(pageURL):
#     pageRequest = requests.get(pageURL)
#     return BeautifulSoup(pageRequest.text, "html.parser")

# def editCardType(dictionary):
#     if (dictionary.get("Card Type") == None):
#         return ({"Card Type": "Normal Unit"})
#     return ({"Grade": dictionary.get("Card Type")})

# def editIllust(dictionary):
#     if (dictionary.get("Illust") == None):
#         return ({"Artist": dictionary.get("Design /  Illust")})
#     else:
#         return ({"Artist": dictionary.get("Illust")})

# def editGrade(dictionary):
#     if (dictionary.get("Grade / Skill") != None):
#         splitGrade = dictionary.get("Grade / Skill").split(" / ")

#         return ({"Grade": (splitGrade[0]).strip()})

#     return ({"Grade": "-"})

# def editSkill(dictionary):
#     if (dictionary.get("Grade / Skill") != None):
#         splitGrade = dictionary.get("Grade / Skill").split(" / ")

#         if (len(splitGrade) > 1):
#             return ({"Skill": (splitGrade[1]).strip()})

#     return ({"Skill": "-"})

# def editTrigger(dictionary):
#     if (dictionary.get("Trigger Effect") != None):
#         triggerEffect = dictionary.get("Trigger Effect").split(" / ")[0]
#         return ({"Trigger Effect": triggerEffect})

#     return ({"Trigger Effect": "-"})

# def editLanguage(dictionary):
#     code = dictionary.get("Card ID")

#     if ("EN" in code):
#         return ({"Language": "EN"})
#     elif ("KR" in code):
#         return ({"Language": "KR"})
#     elif ("TH" in code):
#         return ({"Language": "TH"})
#     elif ("IT" in code):
#         return ({"Language": "IT"})
#     else:
#         return ({"Language": "JP"})

# def editRarity(dictionary):
#     code = dictionary.get("Card ID")

#     if ("(" in code):
#         rarity = code.split("(")[1].strip("()")
#         return ({"Rarity": rarity})
    
#     return ({"Rarity": "-"})

# def editFormat(dictionary):
#     code = dictionary.get("Card ID")

#     if (code[:2] == "V-"):
#         return ({"Format": "V-Premium"})
#     elif (code[:2] == "D-" or code[:3] == "DZ-"):
#         return ({"Format": "Standard"})
#     else:
#         return ({"Format": "Premium"})

# def editSeries(dictionary):
#     code = dictionary.get("Card ID")

#     if (code[:2] == "V-"):
#         return ({"Series": "V Series"})
#     elif (code[:2] == "D-" or code[:3] == "DZ-"):
#         return ({"Series": "D Series"})
#     else:
#         return ({"Series": "Original Series"})

# def editCardID(dictionary):
#     code = dictionary.get("Card ID")
#     return ({"Card ID": code.split(" ")[0]})

# def editSetID(dictionary):
#     code = dictionary.get("Card ID")
#     return ({"Set ID": code.split("/")[0]})

# def readTournamentStatus(cardPageData, dictionary):
#     language = dictionary.get("Language")

#     try:
#         status = cardPageData.find("table", {"class": "tourneystatus"})
#         region = status.find("td", string = language)
#         regulation = region.find_next("td")

#         tourneyStatus = regulation.text.strip()

#         if (tourneyStatus == "Unrestricted"):
#             return ({"Restrictions": tourneyStatus})
#         else:
#             tourneyStatus = ((regulation.find("a")).get("title"))
#             return ({"Restrictions": tourneyStatus})
#     except:
#         return

# def readCardSets(pageData):
#     cardSets = pageData.find("table", {"class": "sets"})
#     setsDescription = (cardSets.find("td")).find_all("li")

#     codeList = []
#     for set in setsDescription:
#         codes = set.get_text(separator = " - ")

#         splitedCodes = codes.split(" - ")
#         splitedCodes = splitedCodes[2:]

#         for code in splitedCodes:
#             codeList.append(code)

#     return codeList

# def readCardEffect(pageData):
#     try:
#         cardEffect = pageData.find("table", {"class": "effect"})
#         effectDescription = cardEffect.find("td")
#         return ({"Card Effect(s)": (effectDescription.text).strip()})
#     except:
#         return ({"Card Effect(s)": "-"})

# def readGiftMarker(pageData):
#     if (pageData.find("a", {"title": "Imaginary Gift/Force"}) != None):
#         return ({"Imaginary Gift": "Force"})
#     elif (pageData.find("a", {"title": "Imaginary Gift/Accel"}) != None):
#         return ({"Imaginary Gift": "Accel"})
#     elif (pageData.find("a", {"title": "Imaginary Gift/Protect"}) != None):
#         return ({"Imaginary Gift": "Protect"})
    
#     return ({"Imaginary Gift": "-"})

# def addAttributes(dictionary, attributes):
#     for index in range(0, len(attributes)):
#         if (index % 2 == 0):
#             title = (attributes[index].text).strip()
#             trait = (attributes[index + 1].text).strip()
#             dictionary.update({title: trait})

#     return dictionary

# def deleteAttributes(dictionary):
#     removeKeywords = ["Kanji", "Kana", "Phonetic", "Thai", "Italian", "Korean", 
#                       "Grade / Skill", "Illust", "Design /  Illust", "Translation"]
    
#     for key in removeKeywords:
#         dictionary.pop(key, None)

#     return dictionary

# def createBasicDictionary(cardPageData, artworksArray):
#     cardMainInfo = cardPageData.find("div", {"class": "info-main"})
#     attributes = cardMainInfo.find_all("td")

#     cardDictionary = {}
#     addAttributes(cardDictionary, attributes)
#     cardDictionary.update(readCardEffect(cardPageData))
#     cardDictionary.update(readGiftMarker(cardMainInfo))
#     cardDictionary.update(editCardType(cardDictionary))
#     cardDictionary.update(editIllust(cardDictionary))
#     cardDictionary.update(editGrade(cardDictionary))
#     cardDictionary.update(editSkill(cardDictionary))
#     cardDictionary.update(editTrigger(cardDictionary))
#     cardDictionary.update(searchArtworks(artworksArray, "Full Art"))
#     deleteAttributes(cardDictionary)

#     return cardDictionary

# def createCardList(cardPageData, basicCard, artworksArray, idArray):
#     cardList = []
    
#     for element in idArray:
#         newCard = basicCard.copy()
#         newCard.update({"Card ID": element})
#         newCard.update(editSeries(newCard))
#         newCard.update(editFormat(newCard))
#         newCard.update(editRarity(newCard))
#         newCard.update(editLanguage(newCard))
#         newCard.update(editSetID(newCard))
#         newCard.update(editCardID(newCard))
#         newCard.update(readTournamentStatus(cardPageData, newCard))
#         # newCard.update(searchArtworks(artworksArray, newCard.get("Card ID")))
#         cardList.append(newCard)
    
#     return cardList

# def cfvReadCard(pageURL):
#     cardPageData = readPage(pageURL)
#     galleryPageData = readPage(createGalleryLink(pageURL))

#     idArray = readCardSets(cardPageData)
#     artworksArray = readFullArts(galleryPageData)

#     basicCard = createBasicDictionary(cardPageData, artworksArray)
#     cardList = createCardList(cardPageData, basicCard, artworksArray, idArray)

#     return cardList

# def cfvScrapeSet(pageURL):
#     setPageData = readPage(pageURL)

#     # Read card page
#     # Find table of all the cards, extract the links
#     # visit each link and read card
    

#     setInfo = setPageData.find("table")
#     print(setInfo)

# # def cfvMain():
# #     columnNames = ["Card ID", "Name", "Card Type", "Grade", "Skill",
# #                     "Imaginary Gift", "Special Icon", "Trigger Effect",
# #                     "Power", "Shield", "Critical", "Nation", "Clan", "Race", 
# #                     "Series", "Format", "Artist", "Card Effect(s)", 
# #                     "Set ID", "Set Name", "Rarity", "Card Art(s)", "Release Date", 
# #                     "Language", "Restrictions", "Full Art(s)"]
# #     createExcel("cfvdatabase.xlsx", "All Cards", columnNames)

# #     list = cfvReadCard("https://cardfight.fandom.com/wiki/Blaster_Blade")
# #     updateExcel("cfvdatabase.xlsx", "All Cards", list)
# #     # sortExcel("cfvdatabase.xlsx", "Language Sorted", "Language")
# #     # updateExcel("cfvdatabase.xlsx", "All Cards", list)
# #     # sortExcel("cfvdatabase.xlsx", "Name Sorted", "Name")

# #     # readSet()









# # def tempReadSetFunction():
# #     tempTable = pd.read_csv("tempSets.txt", sep = "|", names = ["Language", "Code", "Name", "Release Date"])
# #     return tempTable

# # def cfvReadSets():
# #     setsTable = tempReadSetFunction()
# #     return setsTable

# # setData = cfvReadSets()
# # print(setData)

# # data = cfvReadCard("https://cardfight.fandom.com/wiki/Blaster_Blade", setData)
# # print(data)
# # table = pd.DataFrame(data)
# # print(table)


# # for card in data:
# #     value = (card.get("Set ID"))
# #     lang = (card.get("Language"))
# #     print(value)
# #     result = setData.loc[setData["Code"] == value]
# #     release = result["Release Date"]
# #     print("Release Date is " + release)

# # cfvScrapeSet("https://cardfight.fandom.com/wiki/Booster_Set_1:_Descent_of_the_King_of_Knights")

# data = cfvReadCard("https://cardfight.fandom.com/wiki/Blaster_Blade")
# print(data)
# table = pd.DataFrame(data)
# print(table)