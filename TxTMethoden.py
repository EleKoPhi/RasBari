import configparser

from Speicherorte import IniDatei, BarHard, Email

Mischungen = configparser.ConfigParser()
Mischungen.sections()
Mischungen.read(IniDatei)

BarIni = configparser.ConfigParser()
BarIni.sections()
BarIni.read(BarHard)

EmailTxt = configparser.ConfigParser()
EmailTxt.sections()
EmailTxt.read(Email)

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
        return [list(elements) for elements in Mischungen.items(NumberOfDrink)]

    return False

def objectCanBeBuild (NumberOfDrink):
    return Mischungen.has_section(NumberOfDrink)


def getFlag(FlagName):
    flag = BarIni.get("Flags", str(FlagName))
    return int(flag)

def getMailAdress():
    return EmailTxt.get("Gmail","AD")

def getMailPassword():
    return EmailTxt.get("Gmail","PW")

def getAllNamesInList():
    list = ""
    for i in range(11):
        DrinkName = "Drink"+str(i+1)
        if getDrinkName(DrinkName) != "-":
           list = list + "\n-" + getDrinkName((DrinkName))

    return list

def getallBottleStats(Numberofbottle):
    if BarIni.has_section(Numberofbottle):
        return BarIni.items(Numberofbottle)
    else: return False

def changeAmount(BottleNr,newamount):

    BarIni.set("Fluessigkeit"+str(BottleNr),"menge",str(newamount))
    with open(BarHard, 'w') as configfile:
        BarIni.write(configfile)