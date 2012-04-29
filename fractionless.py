from collections import defaultdict
import string
import os

def deckstring(deck):
    return "A" * deck[0] + "B" * deck[1] + "C" * deck[2] + "D" * deck[3] + "E" * deck[4] + "F" * deck[5] + "G" * deck[6] + "H" * deck[7] + "I" * deck[8]

def breakdown(deck):
    return [deck.count("A"),deck.count("B"),deck.count("C"),deck.count("D"),deck.count("E"),deck.count("F"),deck.count("G"),deck.count("H"),deck.count("I")]

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

def gcd(i, j):
    if j == 0:
        return i
    return gcd(j, i % j)

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
                                            yield([a,b,c,d,e,f,g,h,i])

# Hand generator
def hands():
    for a in ranged(0, 7):
        for b in ranged(0, 4):
            for c in ranged(0, 4):
                for d in ranged(0, 7):
                    for e in ranged(0, 4):
                        for f in ranged(0, 4):
                            for g in ranged(0, 4):
                                for h in ranged(0, 7):
                                    for i in ranged(0, 7):
                                        if (a + b + c + d + e + f + g + h + i >= 4 and a + b + c + d + e + f + g + h + i <= 7):
                                            yield([a,b,c,d,e,f,g,h,i])


def evalhand(hand):
    total = 0
    hands = ("AABC", "ABCH", "ACEH", "ACFH", "ABDH", "ADEH", "ADFH", "ADGH", "ABBH", "ABEH", "ABFH", "ABGH", "ABEH", "AEEH", "AEFH", "AEGH", "AEGG", "AEEG", "AEFG")
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
    score[deckstring(i)] = evalhand(deckstring(i))

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
                    temp = ["A","B","C","D","E","F","G","H","I"][i]
                    result[temp] = deck[i] * 1.0 / total
                return result
            else:
                for i in range(0,9):
                    if deck[i] > 0:
                        deck[i] -= 1
                        card = ["A","B","C","D","E","F","G","H","I"][i]
                        tempdeck = deckstring(deck)
                        tempresult = choose(tempdeck, cards - 1)
                        for j in tempresult.keys():
                            temp = string.join(sorted(list(card + j)),"")
                            result[temp] += tempresult[j] * (deck[i] + 1) * 1.0 / total
                            if result[temp] == 0:
                                del result[temp]
                        deck[i] += 1
                return result

        choose = Memoize(choose)

    total7 = 0
    answer = choose(deckstring(deck),7)
    for i in answer.keys():
        total7 += score[i] * answer[i]
    total6 = 0
    answer = choose(deckstring(deck),6)
    for i in answer.keys():
        total6 += score[i] * answer[i]
    total5 = 0
    answer = choose(deckstring(deck),5)
    for i in answer.keys():
        total5 += score[i] * answer[i]
    total4 = 0
    answer = choose(deckstring(deck),4)
    for i in answer.keys():
        total4 += score[i] * answer[i]
    final = total7 + (1 - total7) * total6 + (1 - ((total7 + (1 - total7) * total6))) * total5 + (1 - ((total7 + (1 - total7) * total6 + (1 - ((total7 + (1 - total7) * total6))) * total5))) * total4
    print deck, final
