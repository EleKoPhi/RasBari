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


def proofIngredients(number_of_drink):
    Proof = 0
    Ingredients = Mischungen.items(number_of_drink)

    for i in range(1, len(Ingredients)):
        Proof += int(Ingredients[i][1])

    if Proof <= 100:
        return True
    else:
        return False


def getDrinkName(number_of_drink):
    if Mischungen.has_section(number_of_drink):
        return Mischungen.get(number_of_drink, 'name')

    return "-"


def getAllIngredients(number_of_drink):
    if Mischungen.has_section(number_of_drink):
        return [list(elements) for elements in Mischungen.items(number_of_drink)]

    return False


def objectCanBeBuild(number_of_drink):
    return Mischungen.has_section(number_of_drink)


def getFlag(flag_name):
    flag = BarIni.get("Flags", str(flag_name))
    return int(flag)


def getMailAdress():
    return EmailTxt.get("Gmail", "AD")


def getMailPassword():
    return EmailTxt.get("Gmail", "PW")


def getAllNamesInList():
    list = ""
    for i in range(11):
        DrinkName = "Drink" + str(i + 1)
        if getDrinkName(DrinkName) != "-":
            list = list + "\n-" + getDrinkName((DrinkName))

    return list


def getallBottleStats(numberofbottle):
    if BarIni.has_section(numberofbottle):
        return BarIni.items(numberofbottle)
    else:
        return False


def changeAmount(bottle_nr, new_amount):
    BarIni.set("Fluessigkeit" + str(bottle_nr), "menge", str(new_amount))
    with open(BarHard, 'w') as configfile:
        BarIni.write(configfile)


def getStepper_ini(stepper_id):
    if BarIni.has_section(stepper_id):
        return dict(BarIni.items(stepper_id))
    else:
        print("can't read -> " + stepper_id + " <-")
        return None
