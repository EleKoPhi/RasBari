from random import *
Combinations = ["39","3569","3579"]

class Combination(object):
    element=[]

    def __init__(self,element,posi):
        element[posi]=element


speicherliste={}
buffer=""
enthalteneelemente=0

for a in range(2000):

    buffer=""

    for i in range(0,4):
        buffer=buffer+Combinations[randint(0,2)]

    if buffer in  speicherliste:
        print("schon enthalten")
        continue


    speicherliste[enthalteneelemente]=buffer
    enthalteneelemente+=1





print(speicherliste)
















