from classes.class_Drink import *
from classes.class_Bottle import *
import time


class Bar(object):

    Bottles = []
    DrinkList = []

    errorFlag=0
    productionFlag=0

    dots = [".", "..", "...", "....", "....."]

    progress = 0


    def __init__(self):
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
            print(self.Bottles[i].getname())

        print("\nDrinks inncluded:\n")
        for i in range(0,len(self.DrinkList)):

            if self.DrinkList[i] != False:
                print(self.DrinkList[i].getName())
                print(self.DrinkList[i].WhatsIn())

    def moveSlider(self,direction,speed,position):

        print("Move Slider")
        print("Direction: " + str(direction))
        print("At Speed: " + str(speed))
        print("To Position: " + str(position))

    def getLiquid(self,Liquid,Amount):
        print("Gebe " + str(Amount) + "ml " + str(Liquid) + " aus")

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

    def changeProductionFlag(self,stat):
        if stat == True:
            self.productionFlag = True
        else:
            self.productionFlag = False

    def getErrorFlag(self):
        return self.errorFlag

    def getProductionFlag(self):
        return self.productionFlag

    def mixIt(self,Auswahl):

        self.changeProductionFlag(True)

        if self.DrinkList[Auswahl].getStat() == True:

            print("Start mixing of " + self.DrinkList[Auswahl].getName() + " plase wait")
            self.errorFlag=0

            """for a in range(5):

                for i in range(0, 5):
                    if self.errorFlag == False:
                        print(self.dots[i])
                        sleep(0.5)
                    else:
                        print("Error flage alive")
                        break

                if self.errorFlag == True:
                    self.changeErrorFlag(False)
                    return"""

            self.progress=0

            for i in range(0,100):
                if self.errorFlag == False:
                    self.progress=self.progress+1
                    time.sleep(0.05)
                    if self.progress%10 == 0:
                        print(self.progress)
                else:
                    print("Error flage alive")
                    self.progress=0
                    break

            if self.errorFlag == True:
                self.changeErrorFlag(False)
                return


            print ("Job is done!")


            self.changeProductionFlag(False)

        else:
            print("Drink unknown - Cant mix it")
            self.changeProductionFlag(False)


    def test(self):
        print("Start")
        time.sleep(5)
        print("End")


    def errorFunction(self):
        self.changeErrorFlag(1)
        self.changeProductionFlag(0)

    def getProgress(self):
        return self.progress



















