from TxTMethoden import *

class Bottle(object):

    Bottlestats = []

    def __init__(self, Nummer):
        self.Bottlestats = getallBottleStats("Fluessigkeit" + str(Nummer))
        self.level = int(self.Bottlestats[2][1])

    def getname(self):
        return self.Bottlestats[1][1]

    def getPos(self):
        return self.Bottlestats[3][1]

    def getID(self):
        return self.Bottlestats[0][1]

    def whatsIn(self):
        for i in range(len(self.Bottlestats)):
            print(self.Bottlestats[i])

    def getRest(self):
        return self.Bottlestats[2][1]

    def outputliquid(self,amount):
        print("Open valve")
        print(str(amount) + " "+ self.getname() + "dispenses")
        print("Close valve")

    def openval(self):
        print("open valve")

    def closeval(self):
        print("close valve")

    def degreaseAmount(self,amount):
        newamount = int(self.level)-int(amount)
        self.level=newamount
        changeAmount(int(self.getID()),newamount)

    def resetBottle(self):
        print("-> NEW BOTTLE IN SYSTEM <-")

    def getbottlesize(self):
        return self.Bottlestats[4][1]

    def getRestAmount(self):
        return self.Bottlestats[2][1]

    def putAmount(self,newamount):
        self.level=newamount
        changeAmount(int(self.getID()), newamount)

    def getlevel(self):
        return self.level

    def getliqout(self):
        self.level=0

