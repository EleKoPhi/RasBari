from TxTMethoden import *
from Speicherorte import BarHard

"""BarIni.set("Fluessigkeit1","Name","Gin")

with open(BarHard, 'w') as configfile:
    BarIni.write(configfile)"""

def changeAmount(BottleNr,newamount):
    BarIni.set("Fluessigkeit"+str(BottleNr),"menge",str(newamount))

    with open(BarHard, 'w') as configfile:
        BarIni.write(configfile)


changeAmount(1,)


