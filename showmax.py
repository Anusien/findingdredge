import sqlite3

#for i in ["deck12.sqlite3","deck13.sqlite3","deck14.sqlite3","deck15.sqlite3"]:
for i in ["decks.sqlite3"]:
    conn = sqlite3.connect(i)
    c = conn.cursor()
    c.execute('select * from decks order by perc desc limit 20')
    for j in c.fetchall():
        print j
#    c.execute('select * from decks where c=4 order by perc desc limit 1')
#    for j in c.fetchall():
#        print j
