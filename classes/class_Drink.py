from TxTMethoden import *


class Drink(object):

    Ingredients = []
    alive = False

    def __init__(self, NumberOfDrink):

        allIngredients = getAllIngredients(NumberOfDrink)

        if allIngredients != False:

            if proofIngredients(NumberOfDrink):

                self.Ingredients = allIngredients
                self.alive = True

            else:
                print('Drink over 100%')

        elif allIngredients == False:
            print('Drink unknown')

    def WhatsIn(self):

        if self.alive == True:
            for i in range(len(self.Ingredients)):
                if self.Ingredients[i][1] != '0':
                    print(self.Ingredients[i])

        else:
            print('Drink unknown - cant show whats in')


    def getName(self):
        return self.Ingredients[0][1]

    def getStat(self):
        return self.alive









