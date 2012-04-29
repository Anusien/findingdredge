import Levenshtein
import sqlite3
import sys
import threading
import time
from math import factorial as fact

deckqueue = []
deckqueuelock = threading.Lock()
calc_threads = 2

ioqueue = []
ioqueuelock = threading.Lock()

should_sort = 0

best = 0
maxc = 0
count = 0

class IOThread(threading.Thread):
    def run(self):
        global count, maxc


        conn = sqlite3.connect("decks.sqlite3")
        curs = conn.cursor()
        try:
            curs.execute('''DROP TABLE decks''')
        except:
            pass
        curs.execute('''CREATE TABLE decks
                        (a int, b int, c int, d int, e int, f int, g int, h int, i int, perc float)''')

        while count < maxc:
            while not ioqueue:
                time.sleep(5)
            ioqueuelock.acquire()
            if not ioqueue:
                ioqueuelock.release()
                continue

            i = ioqueue.pop()
            ioqueuelock.release()
            deck = i[0]
            perc = i[1]

            curs.execute('''INSERT INTO decks VALUES (?,?,?,?,?,?,?,?,?,?)''', [deck[0], deck[1], deck[2], deck[3], deck[4], deck[5], deck[6], deck[7], deck[8], perc])
            conn.commit()


class CalculateThread(threading.Thread):
    def run(self):
        global count, best
        time.sleep(1)
        while deckqueue:
            deckqueuelock.acquire()
            if(not deckqueue):
                deckqueue.release()
                continue
            i = deckqueue.pop(0)
            count += 1
            deckqueuelock.release()
            temp = deckCheck(i[0:8])
            ioqueuelock.acquire()
            ioqueue.append([i, temp])
            ioqueuelock.release()
            if temp > best:
                best = temp
                bestdeck = i
                print i, temp, count, maxc
                if should_sort:
                    deckqueuelock.acquire()
                    deckqueue.sort(key = lambda k: Levenshtein.distance(deckstring(k), deckstring(bestdeck)))
                    deckqueuelock.release()

def deckstring(deck):
    return "1" * deck[0] + "2" * deck[1] + "3" * deck[2] + "4" * deck[3] + "5" * deck[4] + "6" * deck[5] + "7" * deck[6] + "8" * deck[7] + "9" * deck[8]


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
    goodHands =[[2, 1, 1, 0, 0, 0, 0, 0],[1, 1, 1, 0, 0, 0, 0, 1],[1, 0, 1, 0, 1, 0, 0, 1],[1, 0, 1, 0, 0, 1, 0, 1],[1, 1, 0, 1, 0, 0, 0, 1],[1, 0, 0, 1, 1, 0, 0, 1],[1, 0, 0, 1, 0, 1, 0, 1],[1, 0, 0, 1, 0, 0, 1, 1],[1, 2, 0, 0, 0, 0, 0, 1],[1, 1, 0, 0, 0, 1, 0, 1],[1, 1, 0, 0, 0, 0, 1, 1],[1, 1, 0, 0, 1, 0, 0, 1],[1, 0, 0, 0, 2, 0, 0, 1],[1, 0, 0, 0, 1, 1, 0, 1],[1, 0, 0, 0, 1, 0, 1, 1],[1, 0, 0, 0, 1, 0, 2, 0],[1, 0, 0, 0, 2, 0, 1, 0],[1, 0, 0, 0, 1, 1, 1, 0]]
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
						break
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

# Main
t = IOThread()
t.start()

for i in range(calc_threads):
    t = CalculateThread()
    t.start()

for i in decks(12, 16):
    deckqueuelock.acquire()
    deckqueue.append(i)
    maxc += 1
    deckqueuelock.release()
