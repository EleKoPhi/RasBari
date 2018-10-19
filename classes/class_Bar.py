
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from classes.class_Drink import *
from classes.class_Bottle import *
import time

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

    def __init__(self):

        QObject.__init__(self)

        for i in range(1, self.checkNumberOfBottles()):
            self.Bottles.extend([Bottle(i)])

        for j in range(0, 12):
            self.DrinkList.extend([False])

        for i in range(0, 12):

            ChoosenDrink = "Drink" + str(i + 1)

            if objectCanBeBuild(ChoosenDrink):
                self.DrinkList[i] = Drink(ChoosenDrink)

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

    def getLiquid(self,Liquid,Amount,Bottle):

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

        self.Bottles[0].degreaseAmount(33)


    def checkNumberOfBottles(self):
        i=1
        while True:
            if BarIni.has_section("Fluessigkeit"+str(i))==False:break
            i=i+1
        return i

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

        if choosen == "CVS":self.changedValSig.emit()
        if choosen == "CAS":self.changedAmountSig.emit()
        if choosen == "CS":self.changedStatus.emit()

    def mixIt(self,Auswahl):

        self.changeProductionFlag(True)

        if self.DrinkList[Auswahl].getStat() == True:

            print("\nStart mixing " + str(self.amount) + " ml " + self.DrinkList[Auswahl].getName() + " plase wait\n")

            self.changeprgress(0)
            self.fuellstand=0

            for i in range(1,len(self.DrinkList[Auswahl].Ingredients)):

                if self.errorFlag==True:break

                liquid_to_get = self.DrinkList[Auswahl].Ingredients[i][0]
                amount_of_liquid = self.DrinkList[Auswahl].Ingredients[i][1]

                if self.DrinkList[Auswahl].Ingredients[i][1] == "0": continue

                else:

                    for i in range(len(self.Bottles)):
                        if(liquid_to_get.upper()==self.Bottles[i].getname().upper()):
                            #self.Bottles[i].degreaseAmount((int(amount_of_liquid)*self.amount*0.01)) #uncomment this line for amount monitoring
                            print(self.Bottles[i].getname() + " menge geaendert")
                            break

                    self.getLiquid(liquid_to_get,amount_of_liquid,self.Bottles[i])

            self.changeErrorFlag(False)
            self.changeProductionFlag(False)

        else:
            print("Drink unknown - Cant mix it")
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










