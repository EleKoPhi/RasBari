from TxTMethoden import *


class Drink(object):

    Ingredients = []
    alive = False

    def __init__(self, Input):

        try:

            allIngredients = getAllIngredients(Input)

            if allIngredients != False:

                if proofIngredients(Input):

                    self.Ingredients = allIngredients

                    self.alive = True

                else:
                    print('Drink over 100%')


            elif allIngredients == False:
                print('Drink unknown')

        except:
            self.Ingredients = Input
            self.alive = True

    def WhatsIn(self):

        if self.alive == True:
            for i in range(len(self.Ingredients)):
                if self.Ingredients[i][1] != '0':
                    print(self.Ingredients[i])
        else:
            print('Drink unknown - cant show whats in')

        return

    def getName(self):
        try:
            return self.Ingredients[0][1]
        except:
            return "could not read that name"

    def getStat(self):
        return self.alive

    def getIngredientString(self):
        string = "Name:" + self.getName() + "\n"
        for i in range(1, len(self.Ingredients)):
            if self.Ingredients[i][1] == "0": continue
            string = string + self.Ingredients[i][0] + ":" + self.Ingredients[i][1] + "\n"

        return string
