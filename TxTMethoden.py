import configparser
from Speicherorte import initial_mixtures, initial_barSetup, initial_email

mixtures = configparser.ConfigParser()
mixtures.sections()
mixtures.read(initial_mixtures)

BarIni = configparser.ConfigParser()
BarIni.sections()
BarIni.read(initial_barSetup)

EmailTxt = configparser.ConfigParser()
EmailTxt.sections()
EmailTxt.read(initial_email)


def get_drink_name(number_of_drink):
    if mixtures.has_section(number_of_drink):
        return mixtures.get(number_of_drink, 'name')

    return "-"

def get_all_ingredients(number_of_drink):
    if mixtures.has_section(number_of_drink):
        return [list(elements) for elements in mixtures.items(number_of_drink)]

    return False

def get_flag(flag_name):
    flag = BarIni.get("Flags", str(flag_name))
    return int(flag)

def get_mail():
    return EmailTxt.get("Gmail", "AD")

def get_password():
    return EmailTxt.get("Gmail", "PW")

def get_stepper_ini(stepper_id):
    if BarIni.has_section(stepper_id):
        return dict(BarIni.items(stepper_id))
    else:
        print("can't read -> " + stepper_id + " <-")
        return None

def get_bottle_properties(bottle_number):
    if BarIni.has_section(bottle_number):
        return BarIni.items(bottle_number)
    else:
        return False

def put_new_level(bottle_nr, new_amount):
    BarIni.set("Fluessigkeit" + str(bottle_nr), "menge", str(new_amount))
    with open(initial_barSetup, 'w') as configfile:
        BarIni.write(configfile)

def proof_ingredients(number_of_drink):
    sum = 0
    ingredients = mixtures.items(number_of_drink)

    for i in range(1, len(ingredients)):
        sum += int(ingredients[i][1])

    if sum == 100:
        return True
    else:
        print(number_of_drink + " can't be loaded to the system")
        return False

def drink_mixture_available(number_of_drink):
    return mixtures.has_section(number_of_drink)
