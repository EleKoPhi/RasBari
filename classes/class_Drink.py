from TxTMethoden import *


# noinspection PyBroadException
class Drink(object):

    def __init__(self, input):

        try:
            allIngredients = get_all_ingredients(input)
            self.Ingredients = allIngredients

        except:
            self.Ingredients = input

    def get_name(self):
        try:
            return self.Ingredients[0][1]
        except:
            print("could not find a drink name")

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

        for i in range(len(self.Ingredients)):
            if self.Ingredients[i][1] != '0':
                print(self.Ingredients[i])
