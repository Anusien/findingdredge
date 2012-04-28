import os
import sys
import sqlite3

if (len(sys.argv) > 1):
    databasename = sys.argv[1]
else:
    print "Specify a database name"
    os._exit(0)    


conn = sqlite3.connect(databasename)
curs = conn.cursor()
try:
    curs.execute('''DROP TABLE decks''')
except:
    pass
curs.execute('''CREATE TABLE decks
                (a int, b int, c int, d int, e int, f int, g int, h int, i int, perc float)''')
conn.commit()
count = 0
best = 0
while (1):
    line = sys.stdin.readline()
    if line.count("done") > 0:
        conn.commit()
        os._exit(0)
    deck = line.split()[3]
    perc = line.split()[4]
    if line.split()[6] > best:
        print line,
        best = line.split()[6]
    curs.execute('''INSERT INTO decks VALUES (?,?,?,?,?,?,?,?,?,?)''',
        [deck.count("A"),
         deck.count("B"),
         deck.count("C"),
         deck.count("D"),
         deck.count("E"),
         deck.count("F"),
         deck.count("G"),
         deck.count("H"),
         deck.count("I"),
         perc])
    count += 1
    if (count % 100 == 0):
        conn.commit()
conn.commit()
