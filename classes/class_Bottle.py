from TxTMethoden import *

class Bottle(object):
    Name = "unbekannt"
    Menge = 0
    Position = 0

    def __init__(self, Nummer):
        self.Name = BarIni.get("Fluessigkeit" + str(Nummer), "name")
        self.Menge = BarIni.get("Fluessigkeit" + str(Nummer), "menge")
        self.Position = BarIni.get("Fluessigkeit" + str(Nummer), "position")

    def getname(self):
        return self.Name