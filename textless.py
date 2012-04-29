from collections import defaultdict
import string
import os

def deckstring(deck):
    return int("1" * deck[0] + "2" * deck[1] + "3" * deck[2] + "4" * deck[3] + "5" * deck[4] + "6" * deck[5] + "7" * deck[6] + "8" * deck[7] + "9" * deck[8])

def breakdown(deck):
    deck = str(deck)
    return [deck.count("1"),deck.count("2"),deck.count("3"),deck.count("4"),deck.count("5"),deck.count("6"),deck.count("7"),deck.count("8"),deck.count("9")]

class Memoize: # stolen from http://code.activestate.com/recipes/52201/
    """Memoize(fn) - an instance which acts like fn but memoizes its arguments
       Will only work on functions with non-mutable arguments
    """
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}
    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.fn(*args)
        return self.memo[args]

# Modified range function, because including the actual max you want is handy.
def ranged(x, y):
    return xrange(x, y + 1)

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
                                            yield(deckstring([a,b,c,d,e,f,g,h,i]))

# Hand generator
def hands():
    for a in ranged(0, 7):
        for b in ranged(0, min(4, 7 - a)):
            for c in ranged(0, min(4, 7 - a - b)):
                for d in ranged(0, min(7, 7 - a - b - c)):
                    for e in ranged(0, min(4, 7 - a - b - c - d)):
                        for f in ranged(0, min(4, 7 - a - b - c - d - e)):
                            for g in ranged(0, min(4, 7 - a - b - c - d - e - f)):
                                for h in ranged(0, min(7, 7 - a - b - c - d - e - f - g)):
                                    for i in ranged(0, min(7, 7 - a - b - c - d - e - f - g - h)):
                                        if (a + b + c + d + e + f + g + h + i >= 4 and a + b + c + d + e + f + g + h + i <= 7):
                                            yield(deckstring([a,b,c,d,e,f,g,h,i]))


def evalhand(hand):
    total = 0
    hand = str(hand)
    hands = ("1123", "1238", "1358", "1368", "1248", "1458", "1468", "1478", "1228", "1258", "1268", "1278", "1558", "1568", "1578", "1577", "1557", "1567")
    for winninghand in hands:
        good = 1
        for card in winninghand:
            if hand.count(card) < winninghand.count(card):
                good = 0
        if good == 1:
            return 1
    return 0

score = {}
for i in hands():
    score[i] = evalhand(i)

count = 0
for deck in decks(12,14):
    if (count % 20 == 0):
        def choose(deck, cards):
            total = 0
            deck = breakdown(deck)
            result = defaultdict(float)
            for i in deck:
                total += i
            if (cards == 1):
                for i in range(0,9):
                    result[i + 1] = deck[i] * 1.0 / total
                return result
            else:
                for i in range(0,9):
                    if deck[i] > 0:
                        deck[i] -= 1
                        card = i + 1
                        tempresult = choose(deckstring(deck), cards - 1)
                        for j in tempresult.keys():
                            temp = deckstring(breakdown(str(card) + str(j)))
                            result[temp] += tempresult[j] * (deck[i] + 1) * 1.0 / total
                            if result[temp] == 0:
                                del result[temp]
                        deck[i] += 1
                return result

        choose = Memoize(choose)

    total7 = 0
    answer = choose(deck,7)
    for i in answer.keys():
        total7 += score[i] * answer[i]
    total6 = 0
    answer = choose(deck,6)
    for i in answer.keys():
        total6 += score[i] * answer[i]
    total5 = 0
    answer = choose(deck,5)
    for i in answer.keys():
        total5 += score[i] * answer[i]
    total4 = 0
    answer = choose(deck,4)
    for i in answer.keys():
        total4 += score[i] * answer[i]
    final = total7 + (1 - total7) * total6 + (1 - ((total7 + (1 - total7) * total6))) * total5 + (1 - ((total7 + (1 - total7) * total6 + (1 - ((total7 + (1 - total7) * total6))) * total5))) * total4
    print breakdown(deck), final
