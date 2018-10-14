import configparser
from Speicherorte import IniDatei, BarHard

Mischungen = configparser.ConfigParser()
Mischungen.sections()
Mischungen.read(IniDatei)

BarIni = configparser.ConfigParser()
BarIni.sections()
BarIni.read(BarHard)

def proofIngredients(NumberOfDrink):
    Proof = 0
    Ingredients=Mischungen.items(NumberOfDrink)

    for i in range(1,len(Ingredients)):
        Proof += int(Ingredients[i][1])

    if Proof<=100:return True
    else: return False

def getDrinkName(NumberOfDrink):

    if Mischungen.has_section(NumberOfDrink):
        return Mischungen.get(NumberOfDrink,'name')

    return "-"

def getAllIngredients(NumberOfDrink):
    if Mischungen.has_section(NumberOfDrink):
        return Mischungen.items(NumberOfDrink)

    return False

def objectCanBeBuild (NumberOfDrink):
    return Mischungen.has_section(NumberOfDrink)

def getGuiWidth():
    return BarIni.get("GUI_Size","x")

def getGuiHight():
    return BarIni.get("GUI_Size","y")







