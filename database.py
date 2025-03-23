import pandas as pd

def dataframe(dictionary):
    return pd.DataFrame.from_dict(dictionary)

def updateFile(newDatabase, name):
    currentDatabase = pd.read_excel(name)
    updatedDatabase = currentDatabase.append(newDatabase, ignore_index = True)
    updatedDatabase.to_excel(name, index = False)