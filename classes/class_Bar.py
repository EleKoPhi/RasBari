import time
from classes.class_Bottle import *
from classes.class_Drink import *
from classes.class_myThread import *
from gobal_variables import *


class Bar(QObject):

    changedValSig = pyqtSignal()
    changedAmountSig = pyqtSignal()
    changedStatus = pyqtSignal()
    missingIngred = pyqtSignal()
    drinkunknown = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)

        self.errorFlag = noError
        self.productionFlag = noProduction

        self.progress = 0
        self.filling_level = 0
        self.cup_size = 300

        self.Bottles = []
        self.DrinkList = []

        for i in range(self.nr_initial_bottles()):
            self.Bottles.extend([Bottle(i)])

        for i in range(self.nr_initial_drinks()):
            choose_drink = "Drink" + str(i)

            if drink_mixture_available(choose_drink):
                if proof_ingredients(choose_drink):
                    self.DrinkList.extend([Drink(choose_drink)])
            else:
                print(choose_drink + " not found in initial file")

        print("\nBar has been initialized")

        print("\nBottles included:\n")
        for i in range(len(self.Bottles)):
            self.Bottles[i].print_whats_in()
            print()

        print("\nDrinks included:\n")
        for i in range(len(self.DrinkList)):
            self.DrinkList[i].print_whats_in()
            print()

    def get_error_flag(self):
        return self.errorFlag

    def get_production_flag(self):
        return self.productionFlag

    def get_progress(self):
        return self.progress

    def get_cup_size(self):
        return self.cup_size

    def get_liquid_position(self, liquid):
        for i in range(len(self.Bottles)):
            if self.Bottles[i].get_name().upper() == liquid.upper():
                return self.Bottles[i].get_position()

        return False

    def nr_initial_bottles(self):
        nur_initial_bottles = 0
        while True:
            if not BarIni.has_section("Fluessigkeit" + str(nur_initial_bottles)): break
            nur_initial_bottles += 1
        return nur_initial_bottles

    def nr_initial_drinks(self):
        nr_initial_drinks = 0
        while True:
            if not mixtures.has_section("Drink" + str(nr_initial_drinks)): break
            nr_initial_drinks += 1
        return nr_initial_drinks

    def move_slider(self, speed, position):

        print("\nMove Slider")
        print("At Speed: " + str(speed))
        print("To Position: " + str(position) + "\n")

    def output_liquid(self, liquid, amount):  # TODO code that function for real output

        amount = int(int(amount) / 100 * self.cup_size)

        self.move_slider("normal", self.get_liquid_position(liquid))

        print("Gebe " + str(int(amount)) + "ml " + str(liquid) + " aus")

        for i in range(amount):
            if self.errorFlag == False:
                if i % 20 == 0: print("Ausgegebene Menge: " + str(i + 10) + " ml")
                self.filling_level = self.filling_level + 1
                self.change_progress(self.filling_level / self.cup_size * 100)
                time.sleep(0.01)
            else:
                print("Error flage alive - Ausgabe abgebrochen")
                return

    def can_be_mixed(self, drink):

        needed_flags = 0
        having_flags = 0

        for i in range(1, len(drink.Ingredients)):  # that part checks, how many ingredients are necessary
            if drink.Ingredients[i][1] != "0":  # for every ingredient in drink != to 0
                needed_flags = needed_flags + 1  # needed_flags is incremented

        for i in range(1, len(drink.Ingredients)):  # Loop all Ingredients
            if drink.Ingredients[i][1] != "0":  # Look only at ingredients != 0
                for j in range(0, len(self.Bottles)):  # Check all bottles
                    if self.Bottles[j].get_name().upper() == drink.Ingredients[i][
                        0].upper():  # if bottle name == ingredient
                        if int(drink.Ingredients[i][1]) * self.cup_size * 0.01 <= int(
                                self.Bottles[j].get_level()):  # check if there is enough liquid reaming
                            having_flags = having_flags + 1  # if we have enough of that, increment having_flags

        if needed_flags == having_flags:
            return True
        else:
            return False

    def mix_drink(self, drink_nr):  # Main function for mixing Drinks - Runns in extra thread

        self.change_ProductionFlag(True)  # If your do that, show the world you work

        if True:  # If Drinklist has that drink + its alive #TODO rework that function, alive flag no longer included

            if self.can_be_mixed(self.DrinkList[drink_nr]):  # check if all ingredients are available

                print("\nStart mixing " + str(self.cup_size) + " ml " \
                      + self.DrinkList[drink_nr].get_name() + " plase wait\n")  # initialize output

                self.change_progress(0)  # reset progress bar
                self.filling_level = 0  # reset "fuellstand

                for i in range(1, len(self.DrinkList[drink_nr].Ingredients)):  # for all ingredients of the drink do ...

                    if self.errorFlag == True: break  # do for the next ingredient, only if errorFlag not true

                    liquid_to_get = self.DrinkList[drink_nr].Ingredients[i][0]
                    amount_of_liquid = self.DrinkList[drink_nr].Ingredients[i][1]

                    if self.DrinkList[drink_nr].Ingredients[i][1] == "0":
                        continue

                    else:

                        for i in range(len(self.Bottles)):
                            if (liquid_to_get.upper() == self.Bottles[i].get_name().upper()):
                                self.Bottles[i].degrease_amount((int(
                                    amount_of_liquid) * self.cup_size * 0.01))  # uncomment this line for amount monitoring
                                break

                        self.output_liquid(liquid_to_get, amount_of_liquid)  # That function getts the liquid

                        print("\n" + self.Bottles[i].get_name() + " menge geaendert")

                self.change_ErrorFlag(False)
                self.change_ProductionFlag(False)

            else:
                self.emit_signal("MI")
                self.change_ProductionFlag(False)

        else:
            self.emit_signal("DUK")
            self.change_ProductionFlag(False)

    def emit_signal(self, signal_id):

        if signal_id == "CVS": self.changedValSig.emit()  # Value for progressbar changed
        if signal_id == "CAS": self.changedAmountSig.emit()  # Amount changed
        if signal_id == "CS": self.changedStatus.emit()  # Status changed
        if signal_id == "MI": self.missingIngred.emit()  # Not all ingredients available
        if signal_id == "DUK": self.drinkunknown.emit()  # Don't know that drink

    def change_ErrorFlag(self, error_status):
        if error_status:
            self.errorFlag = Error
        else:
            self.errorFlag = noError
        self.emit_signal("CS")

    def change_ProductionFlag(self, production_status):
        if production_status:
            self.productionFlag = Production
        else:
            self.productionFlag = noProduction
        self.emit_signal("CS")

    def errorFunction(self):
        self.change_ErrorFlag(1)
        self.change_ProductionFlag(0)

    def change_volume(self, amount):
        if (self.productionFlag == False) & (self.cup_size + amount >= 20) & (self.cup_size + amount <= 999):
            self.cup_size = self.cup_size + amount
            self.emit_signal("CAS")

    def change_progress(self, new_progress):
        self.progress = new_progress
        self.emit_signal("CVS")

    def get_all_drinks_string(self):
        drinks_string = ""

        for i in range(len(self.DrinkList)):
            line = "Drink " + str(i) + ": " + self.DrinkList[i].get_name() + "\n"
            drinks_string = drinks_string + line

        return drinks_string




