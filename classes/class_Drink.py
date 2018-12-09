from TxTMethoden import *


class Drink(object):

    def __init__(self, input):

        try:
            allIngredients = getAllIngredients(input)

            if allIngredients:
                if proofIngredients(input):
                    self.Ingredients = allIngredients
                    self.alive = True
                else:
                    print('Drink over 100%')
            elif allIngredients == False:
                print('Drink unknown')
        except:
            self.Ingredients = input
            self.alive = True

    def get_name(self):
        try:
            return self.Ingredients[0][1]
        except:
            print("could not find a drink name")

    def get_drink_status(self):
        return self.alive

    def get_ingredient_string(self):
        string = "Name:" + self.get_name() + "\n"
        for i in range(1, len(self.Ingredients)):
            if self.Ingredients[i][1] == "0": continue
            string = string + self.Ingredients[i][0] + ":" + self.Ingredients[i][1] + "\n"

        return string

    def put_new_ingredients(self, new_ingredients):

        self.Ingredients[1:(len(self.Ingredients))] = []

        for i in range(len(new_ingredients)):
            self.Ingredients.extend([new_ingredients[i]])

    def print_whats_in(self):

        if self.alive:
            for i in range(len(self.Ingredients)):
                if self.Ingredients[i][1] != '0':
                    print(self.Ingredients[i])
        else:
            print('Drink unknown - cant show whats in')
