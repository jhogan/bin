#! /usr/bin/python
import random
import sys

class pocket:
    def __init__(self, no):
        self._no=no

    def color(self):
        no=self._no
        even = self.iseven()

        if no in range(-1,1): return 'g'

        if no in range(1, 11) + range(19,29):
            return ['r', 'b'][even]
        else:
            return ['b', 'r'][even]
    def iseven(self):
        return (self._no % 2) == 0
            
class wheel:
    def __init__(self):
        self._pockets=[]
        for i in range(-1,37):
            p = pocket(i)
            self._pockets.append(p)

    def spin(self):
        rand=random.randint(-1, 36)
        p= self.getpocket(rand)
        if p == None: print ("r: %s" % rand)

        return p
            


    def getpocket(self, no):
        for p in self._pockets:
            if p._no == no: return p

class player:
    def __init__(self):
        self._amt=100.0
        self._wheel=wheel()
        self._mult=2.0
        self._bet=1.0
    
    def play(self):
        w=self._wheel
        p=w.spin()
        bet=self._bet
        if p.iseven():
            self._amt += bet
            self._bet=1.0
            return True
        else:
            self._amt -= bet
            self._bet *= self._mult
            return False
            
        










































pl=player()
rounds=200
plays=0; maxplaytotal=0
for round in range (0, rounds+1):
    i=0; maxplay=0
    m=0
    pl._amt=100.0; pl._bet=.50
    while pl._amt>0:
        play=pl.play()
        print("\t%s %s %s" % (pl._amt, pl._bet, ['BAD', 'OK '][play]))
        if m < pl._amt: 
            m=pl._amt
            maxplay=i
        i+=1
    print ("T: %s, %s %s" % (m,maxplay,i))
    plays+=i
    maxplaytotal += maxplay


print "plays: %s; %s" % (plays, maxplaytotal/rounds)

    
