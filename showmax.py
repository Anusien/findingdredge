import sqlite3

#for i in ["deck12.sqlite3","deck13.sqlite3","deck14.sqlite3","deck15.sqlite3"]:
for i in ["decks.sqlite3"]:
    conn = sqlite3.connect(i)
    c = conn.cursor()
    print "Best 10 decks:"
    c.execute('select * from decks order by perc desc limit 10')
    for j in c.fetchall():
        print j
    print
    
    print "Best 12-chaff deck:",
    c.execute('select * from decks where i = 12 order by perc desc limit 1')
    for j in c.fetchall():
        print j
    print "Best 12-chaff, 4 LED deck:",
    c.execute('select * from decks where i = 12 and c = 4 order by perc desc limit 1')
    for j in c.fetchall():
        print j
    print "Best 13-chaff deck:",
    c.execute('select * from decks where i = 13 order by perc desc limit 1')
    for j in c.fetchall():
        print j
    print "Best 13-chaff, 4 LED deck:",
    c.execute('select * from decks where i = 13 and c = 4 order by perc desc limit 1')
    for j in c.fetchall():
        print j
    print "Best 14-chaff deck:",
    c.execute('select * from decks where i = 14 order by perc desc limit 1')
    for j in c.fetchall():
        print j
    print "Best 14-chaff, 4 LED deck:",
    c.execute('select * from decks where i = 14 and c = 4 order by perc desc limit 1')
    for j in c.fetchall():
        print j
    print "Best 15-chaff deck:",
    c.execute('select * from decks where i = 15 order by perc desc limit 1')
    for j in c.fetchall():
        print j
    print "Best 15-chaff, 4 LED deck:",
    c.execute('select * from decks where i = 12 and c = 4 order by perc desc limit 1')
    for j in c.fetchall():
        print j
    
#    c.execute('select * from decks where c=4 order by perc desc limit 1')
#    for j in c.fetchall():
#        print j
