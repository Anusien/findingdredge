import commands
import shutil
import time
import os
import string
import sys
import Levenshtein
import string

class Memoize: # stolen from http://code.activestate.com/recipes/52201/
    """Memoize(fn) - an instance which acts like fn but memoizes its arguments
       Will only work on functions with non-mutable arguments
    """
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}
    def __call__(self, *args):
        if not self.memo.has_key(args):
            self.memo[args] = self.fn(*args)
        return self.memo[args]

mini = 12
maxi = 14
if (len(sys.argv) > 1):
    mini = int(sys.argv[1])
    maxi = int(sys.argv[1])


# Modified range function, because including the actual max you want is handy.
def ranged(x, y):
    for z in xrange(x, y + 1):
        yield z

# Deck generator
def decks(mini = 12, maxi = 14):
    for a in ranged(5, 12):
        for b in ranged(0, 4):
            for c in ranged(0, 4):
                for d in ranged(0, 12):
                    for e in ranged(0, 4):
                        for f in ranged(0, 4):
                            for g in ranged(0, 4):
                                for h in ranged(0, 16):
                                    for i in ranged(mini, maxi):
                                        if (a + b + c + d + e + f + g + h + i == 60):
                                            yield ("A" * a + "B" * b + "C" * c + "D" * d + "E" * e + "F" * f + "G" * g + "H" * h + "I" * i)

def deckeval(deck):
    def pullcard(deck,handsize,pulledsofar):
        total = 0
        hands = ("AABC", "ABCH", "ACEH", "ACFH", "ABDH", "ADEH", "ADFH", "ADGH", "ABBH", "ABEH", "ABFH", "ABGH", "ABEH", "AEEH", "AEFH", "AEGH", "AEGG", "AEEG", "AEFG")
        if (handsize == pulledsofar.__len__()):
            for winninghand in hands:
                good = 1
                for card in winninghand:
                    if pulledsofar.count(card) < winninghand.count(card):
                        good = 0
                if good == 1:
                    return 1
            return 0
        for i in range(0, deck.__len__()):
            pulledsofarcopy = pulledsofar
            if i == 0:
                deckcopy = deck[1:]
            else:
                if i == deck.__len__() - 1:
                    deckcopy = deck[:deck.__len__() - 1]
                else:
                    deckcopy = deck[0:i] + deck[i+1:]
            pulledsofarcopy += deck[i]
            pulledsofarcopy = string.join(((sorted(pulledsofarcopy))),"")
            total += pullcard(deckcopy, handsize, pulledsofarcopy)
        return total

    pullcard = Memoize(pullcard)

    d7 = pullcard(deck,7,"")
    d6 = pullcard(deck,6,"")
    d5 = pullcard(deck,5,"")
    d4 = pullcard(deck,4,"")
    decksize = deck.__len__()
    oddsofgood7 = (d7 * 1.0 / ((decksize) * (decksize - 1) * (decksize - 2) * (decksize - 3) * (decksize - 4) * (decksize - 5) * (decksize - 6)))
    oddsofgood6 = (d6 * 1.0 / ((decksize) * (decksize - 1) * (decksize - 2) * (decksize - 3) * (decksize - 4) * (decksize - 5)))
    oddsofgood5 = (d5 * 1.0 / ((decksize) * (decksize - 1) * (decksize - 2) * (decksize - 3) * (decksize - 4)))
    oddsofgood4 = (d4 * 1.0 / ((decksize) * (decksize - 1) * (decksize - 2) * (decksize - 3)))
    return oddsofgood7 + (1 - oddsofgood7) * oddsofgood6 + (1 - ((oddsofgood7 + (1 - oddsofgood7) * oddsofgood6))) * oddsofgood5 + (1 - ((oddsofgood7 + (1 - oddsofgood7) * oddsofgood6 + (1 - ((oddsofgood7 + (1 - oddsofgood7) * oddsofgood6))) * oddsofgood5))) * oddsofgood4

conn = dict()
c = dict()

max = 0
maxc = 0
fcount = 0

queue = []
for i in decks(mini,maxi):
    queue.append(i)

count = 0
bestdeck = ""
bestperc = 0

while (len(queue) > 0):
    deck = queue.pop(0)
    count += 1
    icount = deck.count("I")
    perc = deckeval(deck)
    if perc > bestperc:
        bestperc = perc
        bestdeck = deck
        queue = sorted(queue, key = lambda k: Levenshtein.distance(k, bestdeck))
    print icount, count, maxc, deck, perc, bestdeck, bestperc

print "done"
