# import json
# import pymongo

# def createDatabase(name):
#     client = pymongo.MongoClient("")
#     database = client[name]

#     collection = database["Cards"]

# def dictionaryToJSON(card):
#     return json.dumps(card)

# def makeJSONList(cardList):
#     transformedList = []

#     for element in cardList:
#         transformedList.append(dictionaryToJSON(element))

#     return transformedList

# def addToDatabase(JSONList):
#     collection.insert_many(JSONList)