from TxTMethoden import *


class Bottle(object):

    def __init__(self, number):
        self.bottle_property = get_bottle_properties("Fluessigkeit" + str(number))  # all properties of that bottle
        self.level = int(self.bottle_property[2][1])  # the current amount of liquid in that bottle

    def get_ID(self):
        return self.bottle_property[0][1]

    def get_name(self):
        return self.bottle_property[1][1]

    def get_remaining_content(self):
        return self.bottle_property[2][1]

    def get_position(self):
        return self.bottle_property[3][1]

    def get_bottle_size(self):
        return self.bottle_property[4][1]

    def get_level(self):
        return self.level

    def put_level_zero(self):
        self.level = 0

    def put_amount(self, new_amount):
        self.level = new_amount
        put_new_level(int(self.get_ID()), new_amount)

    def degrease_amount(self, amount):
        new_amount = int(self.level) - int(amount)
        self.level = new_amount
        put_new_level(int(self.get_ID()), new_amount)

    def open_valve(self):  # TODO include the GPIO function here
        print("open valve")

    def close_valve(self):  # TODO include the GPIO function here
        print("close valve")

    def dispense_liquid(self, amount):  # TODO include the real application here
        self.open_valve()
        print(str(amount) + " " + self.get_name() + "dispenses")
        self.close_valve()

    def print_whats_in(self):
        for i in range(len(self.bottle_property)):
            print(self.bottle_property[i])