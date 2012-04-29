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
        if not self.memo.has_key(args):
            self.memo[args] = self.fn(*args)
        return self.memo[args]

def gcd(i, j):
    if j == 0:
        return i
    return gcd(j, i % j)

class frac:

    def __init__(self, num = 0, den = 1):
        self.num = num
        self.den = den
        self.simplify()
    
    def __add__(self, other):
        return frac(self.num * other.den + other.num * self.den, self.den * other.den).simplify()

    def __sub__(self, other):
        return frac(self.num * other.den - other.num * self.den, self.den * other.den).simplify()
    
    def __mul__(self, other):
        return frac(self.num * other.num, self.den * other.den).simplify()

    def __div__(self, other):
        return frac(self.num * other.den, self.den * other.num).simplify()

    def simplify(self):
        temp = gcd(self.num, self.den)
        self.num /= temp
        self.den /= temp
        return self
    
    def __repr__(self):
        if (self.den == 1):
            return str(self.num)
#        return str(self.num) + " / " + str(self.den), 
        return str(self.num * 1.0 / self.den)

    
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


def choose(deck, cards):
    total = 0
    deck = breakdown(deck)
    result = {}
    for i in deck:
        total += i
    if (cards == 1):
        for i in range(0,9):
            temp = ["A","B","C","D","E","F","G","H","I"][i]
            result[temp] = frac(deck[i],total)
        return result
#        for i in result.keys():
#            if (result[i].num > 0):
#                yield([i,result[i]])
    else:
        for i in range(0,9):
            if deck[i] > 0:
                deck[i] -= 1
                card = ["A","B","C","D","E","F","G","H","I"][i]
                tempdeck = deckstring(deck)
                tempresult = choose(tempdeck, cards - 1)
                for j in tempresult.keys():
                    temp = string.join(sorted(list(card + j)),"")
                    if result.has_key(temp):
                        result[temp] += tempresult[j] * frac(deck[i] + 1,total)
                    else:
                        result[temp] = tempresult[j] * frac(deck[i] + 1,total)
                    if result[temp] == 0:
                        del result[temp]
                deck[i] += 1
#        for i in result.keys():
#            if (result[i].num > 0):
#                yield([i,result[i]])
        return result

choose = Memoize(choose)

def evalhand(hand):
    total = 0
    hands = ("AABC", "ABCH", "ACEH", "ACFH", "ABDH", "ADEH", "ADFH", "ADGH", "ABBH", "ABEH", "ABFH", "ABGH", "ABEH", "AEEH", "AEFH", "AEGH", "AEGG", "AEEG", "AEFG")
    for winninghand in hands:
        good = 1
        for card in winninghand:
            if hand.count(card) < winninghand.count(card):
                good = 0
        if good == 1:
            return frac(1, 1)
    return frac(0, 1)

evalhand = Memoize(evalhand)

for deck in decks(12,14):
#if (1):
#    deck = [12, 4, 0, 7, 4, 4, 4, 13, 12]
    total = frac(0, 1)
    answer = choose(deckstring(deck),7)
    for i in sorted(answer.keys()):
        total += evalhand(i) * answer[i]
    total7 = total
    total = frac(0, 1)
    answer = choose(deckstring(deck),6)
    for i in sorted(answer.keys()):
        total += evalhand(i) * answer[i]
    total6 = total
    total = frac(0, 1)
    answer = choose(deckstring(deck),5)
    for i in sorted(answer.keys()):
        total += evalhand(i) * answer[i]
    total5 = total
    total = frac(0, 1)
    answer = choose(deckstring(deck),4)
    for i in sorted(answer.keys()):
        total += evalhand(i) * answer[i]
    total4 = total
    final = total7 + (frac(1, 1) - total7) * total6 + (frac(1, 1) - ((total7 + (frac(1, 1) - total7) * total6))) * total5 + (frac(1, 1) - ((total7 + (frac(1, 1) - total7) * total6 + (frac(1, 1) - ((total7 + (frac(1, 1) - total7) * total6))) * total5))) * total4
    print deck, final
