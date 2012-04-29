import sqlite3
import sys

if len(sys.argv) < 2:
    sys.exit(0)

deck = [0,0,0,0,0,0,0,0,0]

for i in range(8):
    deck[i] = 0

if len(sys.argv) == 2:
    for c in sys.argv[1]:
        if c == 'A':
            deck[0] += 1
        if c == 'B':
            deck[1] += 1
        if c == 'C':
            deck[2] += 1
        if c == 'D':
            deck[3] += 1
        if c == 'E':
            deck[4] += 1
        if c == 'F':
            deck[5] += 1
        if c == 'G':
            deck[6] += 1
        if c == 'H':
            deck[7] += 1
        if c == 'I':
            deck[8] += 1

if len(sys.argv) > 2:
    for c in range(len(sys.argv)):
        if c == 0:
            continue
        deck[c-1] = sys.argv[c]

#for i in ["deck12.sqlite3","deck13.sqlite3","deck14.sqlite3","deck15.sqlite3"]:
for i in ["decks.sqlite3"]:
    conn = sqlite3.connect(i)
    c = conn.cursor()


    print "Looking up that deck"
    #c.execute
    out_str = 'select * from decks where A = ' + str(deck[0]) + ' and B = ' + str(deck[1]) + ' and C = ' + str(deck[2]) + ' and D = ' + str(deck[3]) + ' and E = ' + str(deck[4]) + ' and F = ' + str(deck[5]) + ' and G = ' + str(deck[6]) + ' and H = ' + str(deck[7]) + ' and I = ' + str(deck[8])
    c.execute(out_str)
    #print out_str
    for j in c.fetchall():
        print j
