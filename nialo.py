import Levenshtein
import sqlite3

def deckstring(deck):
    return "1" * deck[0] + "2" * deck[1] + "3" * deck[2] + "4" * deck[3] + "5" * deck[4] + "6" * deck[5] + "7" * deck[6] + "8" * deck[7] + "9" * deck[8]

conn = sqlite3.connect("decks.sqlite3")
curs = conn.cursor()
try:
    curs.execute('''DROP TABLE decks''')
except:
    pass
curs.execute('''CREATE TABLE decks
                (a int, b int, c int, d int, e int, f int, g int, h int, i int, perc float)''')


from math import factorial as fact

def ranged(x, y):
    return xrange(x, y + 1)

def comb(n, k):
    if (k > n):
        return 0
    else:
        if (k == n):
            return 1
        else:
            #print(n)
            #print(k)
            return ((fact(n))/((fact(k))*(fact(n-k))))

#prob ABNNNNN = (A C copies(A) * B C copies(B) * N C copies(N) over 7 C decksize
def probn(decksize, copies, minC, maxC, hand):
    n = len(copies)
    denominator = comb(decksize,hand) * 1.0
    res = 0.0
    remDeck = decksize - sum(copies)
    tempMin = list(minC)
    looping = 1
    while (looping == 1):
        numerator = 1.0
        for i in range(n):
            numerator = numerator * comb(copies[i],tempMin[i])
        numerator = numerator * comb(remDeck,(hand - sum(tempMin)))
        res = res + (numerator/denominator)
        #looping logic
        if(n > 2):
            for j in range(n):
                if((tempMin[j] == maxC[j]) or (sum(tempMin) == hand)):
                    tempMin[j] = minC[j]
                    if (j == (n-1)):
                        looping = 0
                else:
                    hand[j] += 1
        #silly special cases cause python is silly
        #omitted cause I'm lazy
    return res

def deckCheck(deck):
    counter = 0
    mins = [1,0,0,0,0,0,0,0]
    hand = list(mins)
    mulledTo = 1
    final = 0
    goodHands =[[2, 1, 1, 0, 0, 0, 0, 0],[1, 1, 1, 0, 0, 0, 0, 1],[1, 0, 1, 0, 1, 0, 0, 1],[1, 0, 1, 0, 0, 1, 0, 1],[1, 1, 0, 1, 0, 0, 0, 1],[1, 0, 0, 1, 1, 0, 0, 1],[1, 0, 0, 1, 0, 1, 0, 1],[1, 0, 0, 1, 0, 0, 1, 1],[1, 2, 0, 0, 0, 0, 0, 1],[1, 1, 0, 0, 1, 0, 0, 1],[1, 1, 0, 0, 0, 1, 0, 1],[1, 1, 0, 0, 0, 0, 1, 1],[1, 1, 0, 0, 1, 0, 0, 1],[1, 0, 0, 0, 2, 0, 0, 1],[1, 0, 0, 0, 1, 1, 0, 1],[1, 0, 0, 0, 1, 0, 1, 1],[1, 0, 0, 0, 1, 0, 2, 0],[1, 0, 0, 0, 2, 0, 1, 0],[1, 0, 0, 0, 1, 1, 1, 0]]
    for h in [7, 6, 5, 4]:
        p = 0
        looping = 1
        while(looping == 1):
            #check if hand is 'good'
            for goodHand in goodHands:
                good = 1
                for i in range(8):
                    if (hand[i] < goodHand[i]):
                        good = 0
                if (good == 1):
                    p = p + probn(60,deck,hand,hand,h)
                    break
            #looping logic
            for j in range(8):
                if ((hand[j] == deck[j]) or (sum(hand) == h)):
                        hand[j] = mins[j]
                        if(j == 7):
                            looping = 0
                else:
                    hand[j] += 1
                    break
        final = final + mulledTo * p
        mulledTo = 1 - final
    return final

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

best = 0

queue = []
for i in decks(12, 16):
    queue.append(i)

while (len(queue) > 0):
    i = queue.pop(0)
    temp = deckCheck(i[0:8])
    if temp > best:
        best = temp
        bestdeck = i
        print i, temp
        queue = sorted(queue, key = lambda k: Levenshtein.distance(deckstring(k), deckstring(bestdeck)))
    curs.execute('''INSERT INTO decks VALUES (?,?,?,?,?,?,?,?,?,?)''', [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], temp])
    conn.commit()