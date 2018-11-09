import time

from classes.class_Bottle import *
from classes.class_Drink import *
from classes.class_myThread import *


class Bar(QObject):

    Bottles = []
    DrinkList = []

    errorFlag=0
    productionFlag=0
    progress = 0
    amount = 300
    fuellstand = 0

    changedValSig = pyqtSignal()
    changedAmountSig = pyqtSignal()
    changedStatus = pyqtSignal()
    missingIngred = pyqtSignal()
    drinkunknown = pyqtSignal()

    def __init__(self):

        QObject.__init__(self)

        for i in range(1, self.numberOfBottles()):
            self.Bottles.extend([Bottle(i)])

        for i in range(1, self.NumberOfDrinks() + 1):

            ChoosenDrink = "Drink" + str(i)

            if objectCanBeBuild(ChoosenDrink):
                self.DrinkList.extend([Drink(ChoosenDrink)])

        print("\nBar has been initialized")

        print("\nBottles included:\n")
        for i in range(0,len(self.Bottles)):
            self.Bottles[i].whatsIn()
            print()

        print("\nDrinks inncluded:\n")
        for i in range(0,len(self.DrinkList)):

            if self.DrinkList[i] != False:
                print(self.DrinkList[i].getName())
                self.DrinkList[i].WhatsIn()
                print()

    def moveSlider(self,direction,speed,position):

        print("\nMove Slider")
        print("Direction: " + str(direction))
        print("At Speed: " + str(speed))
        print("To Position: " + str(position) + "\n")

    def getLiquid(self,Liquid,Amount): # TODO code that function for real output

        Amount=int(int(Amount)/100*self.amount)

        self.moveSlider("right", "normal", self.getPosition(Liquid))

        print("Gebe " + str(int(Amount)) + "ml " + str(Liquid) + " aus")

        for i in range(Amount):
            if self.errorFlag == False:
                if i%20==0:print("Ausgegebene Menge: " + str(i+10) + " ml")
                self.fuellstand = self.fuellstand+1
                self.changeprgress(self.fuellstand/self.amount*100)
                time.sleep(0.01)
            else:
                print("Error flage alive - Ausgabe abgebrochen")
                return

    def numberOfBottles(self):
        i=1
        while True:
            if BarIni.has_section("Fluessigkeit"+str(i))==False:break
            i=i+1
        return i

    def NumberOfDrinks(self):
        i = 1
        while True:
            if Mischungen.has_section("Drink" + str(i)) == False: break
            i = i + 1
        return i - 1


    def ReadBottleInit(self,BottleNum):
        return BarIni.items(BottleNum)

    def changeErrorFlag(self,stat):
        if stat == True:
            self.errorFlag = True
        else:
            self.errorFlag = False
        self.sendSignal("CS")

    def changeProductionFlag(self,stat):
        if stat == True:
            self.productionFlag = True
        else:
            self.productionFlag = False
        self.sendSignal("CS")

    def getErrorFlag(self):
        return self.errorFlag

    def getProductionFlag(self):
        return self.productionFlag

    def sendSignal(self,choosen):

        if choosen == "CVS":self.changedValSig.emit()       #Value for progressbar changed
        if choosen == "CAS":self.changedAmountSig.emit()    #Amount changed
        if choosen == "CS":self.changedStatus.emit()        #Status changed
        if choosen == "MI":self.missingIngred.emit()        #Not all ingredients available
        if choosen == "DUK":self.drinkunknown.emit()        #Don't know that drink

    def mixIt(self,Auswahl):    #Main function for mixing Drinks - Runns in extra thread

        self.changeProductionFlag(True) #If your do that, show the world you work

        if self.DrinkList[Auswahl].getStat() == True: #If Drinklist has that drink + its alive

            if self.canbemixed(self.DrinkList[Auswahl]): #check if all ingredients are available

                print("\nStart mixing " + str(self.amount) + " ml " \
                      + self.DrinkList[Auswahl].getName() + " plase wait\n") #initialize output

                self.changeprgress(0)   #reset progress bar
                self.fuellstand=0       #reset "fuellstand

                for i in range(1,len(self.DrinkList[Auswahl].Ingredients)): #for all ingredients of the drink do ...

                    if self.errorFlag==True:break   #do for the next ingredient, only if errorFlag not true

                    liquid_to_get = self.DrinkList[Auswahl].Ingredients[i][0]
                    amount_of_liquid = self.DrinkList[Auswahl].Ingredients[i][1]

                    if self.DrinkList[Auswahl].Ingredients[i][1] == "0": continue

                    else:

                        for i in range(len(self.Bottles)):
                            if(liquid_to_get.upper()==self.Bottles[i].getname().upper()):
                                self.Bottles[i].degreaseAmount((int(amount_of_liquid)*self.amount*0.01)) #uncomment this line for amount monitoring
                                break

                        self.getLiquid(liquid_to_get,amount_of_liquid) #That function getts the liquid

                        print("\n" + self.Bottles[i].getname() + " menge geaendert")

                self.changeErrorFlag(False)
                self.changeProductionFlag(False)

            else:
                self.sendSignal("MI")
                self.changeProductionFlag(False)

        else:
            self.sendSignal("DUK")
            self.changeProductionFlag(False)

    def errorFunction(self):
        self.changeErrorFlag(1)
        self.changeProductionFlag(0)

    def getProgress(self):
        return self.progress

    def getAmount(self):
        return self.amount

    def change_volume(self, amount):
        if (self.productionFlag == False) & (self.amount+amount >= 20) & (self.amount+amount <= 999):
            self.amount = self.amount+amount
            self.sendSignal("CAS")

    def changeprgress(self,newval):
        self.progress=newval
        self.sendSignal("CVS")


    def getPosition(self,liquid):
        for i in range(len(self.Bottles)):
            if self.Bottles[i].getname().upper()==liquid.upper():
                return self.Bottles[i].getPos()

        return False

    def canbemixed(self,Drink):

        Flagneed = 0
        Flaghave = 0

        for i in range(1, len(Drink.Ingredients)):  #that part checks, how many ingredients are necessary
            if Drink.Ingredients[i][1] != "0":      #for every ingredient in drink != to 0
                Flagneed=Flagneed+1                 #Flagneed is incremented

        for i in range(1,len(Drink.Ingredients)):   #Loop all Ingredients
            if Drink.Ingredients[i][1] != "0":      #Look only at ingredients != 0
                for j in range(0,len(self.Bottles)):     #Check all bottles
                    if self.Bottles[j].getname().upper() == Drink.Ingredients[i][0].upper(): #if bottle name == ingredient
                        if int(Drink.Ingredients[i][1])*self.amount*0.01 <= int(self.Bottles[j].getlevel()): #check if there is enought liquid remaing
                            Flaghave = Flaghave+1   #if we have enought of that, increment Flagehave

        if Flagneed == Flaghave: return True
        else: return False
