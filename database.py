import pandas as pd

def dictionaryToDataframe(dictionary):
    return pd.DataFrame.from_dict(dictionary)

def updateFile(newDatabase, name):
    try:
        currentDatabase = pd.read_excel(name)
        updatedDatabase = currentDatabase.append(newDatabase, ignore_index = True)
        updatedDatabase.to_excel(name, index = False)
    except:
        newDatabase.to_excel(name, index = False)
