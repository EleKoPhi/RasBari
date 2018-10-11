from classes.class_Drink import *
from classes.class_Bottle import *


class Bar(object):

    Bottles = []
    DrinkList = []
    Threads = []

    def __init__(self):
        for i in range(1, self.checkNumberOfBottles()):
            self.Bottles.extend([Bottle(i)])

        for j in range(0, 12):
            self.DrinkList.extend([False])

        for i in range(0, 12):

            ChoosenDrink = "Drink" + str(i + 1)

            if objectCanBeBuild(ChoosenDrink):
                self.DrinkList[i] = Drink(ChoosenDrink)

        print("Bar has been initialized")

        print("\nBottles included:")
        for i in range(0,len(self.Bottles)):
            print(self.Bottles[i].getname())

        print("\nDrinks inncluded:")
        for i in range(0,len(self.DrinkList)):
            if self.DrinkList[i] != False:
                print(self.DrinkList[i].getName)
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










