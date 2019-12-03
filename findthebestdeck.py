from math import factorial
import json
import multiprocessing.queues
import sqlite3
import sys
import time

# Globals
cardtypes = []
goodhands = []
numcardtypes = 0
cardtypes_map = dict()

json_filename = "dredge.json"

with open(json_filename) as json_file:
    json_data = json.load(json_file)
    i = 0
    for cardtype in json_data["cards"]:
        identifier = cardtype["id"]
        name = cardtype["name"]
        minimum = int(cardtype.get("minimum", "0"))
        maximum = int(cardtype.get("maximum", "4"))

        if identifier in cardtypes_map:
            raise ValueError("Duplicate identifier " + identifier)

        cardtypes.append([name, minimum, maximum])
        cardtypes_map[identifier] = i
        i += 1
        numcardtypes = len(cardtypes)

    for hand in json_data["hands"]:
        goodhand = [0] * numcardtypes
        for card, number in hand.items():
            if number < 0:
                raise ValueError("Illegal hand requiring " + str(number) + " of " + card)
            index = cardtypes_map[card]
            goodhand[index] = number
        goodhands.append(goodhand)

# Run-time constants
dbname = json_filename + ".sqlite3"


class Memoize:  # stolen from http://code.activestate.com/recipes/52201/
    """Memoize(fn) - an instance which acts like fn but memoizes its arguments
       Will only work on functions with non-mutable arguments
    """

    def __init__(self, fn):
        self.fn = fn
        self.memo = {}

    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.fn(*args)
        return self.memo[args]


def SQLLogDeck(cursor, connection, deck, perc):
    sql = "INSERT INTO decks VALUES ("
    for card in range(len(deck)):
        sql = ''.join([sql, str(deck[card]) + ", "])
    sql = ''.join([sql, str(perc) + ")"])
    cursor.execute(sql)
    success = 0
    while not success:
        try:
            connection.commit()
            success = 1
            break
        except sqlite3.OperationalError:
            pass


def ProcessDeckCheck(deck):
    perc = deckCheck(deck)
    ProcessDeckCheck.ioqueue.put([deck, perc])
    return perc


def ProcessDeckCheck_init(ioqueue):
    ProcessDeckCheck.ioqueue = ioqueue


def ProcessIO(ioqueue):
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()

    count = 0
    bestperc = 0.0

    while 1:
        if ioqueue.empty():
            time.sleep(5)
            if count == 0:
                continue
            if ioqueue.empty():
                print("Completed ", count, " decks")
                return count
        temp = ioqueue.get()
        count += 1
        deck = temp[0]
        perc = temp[1]
        if perc > bestperc:
            bestperc = perc
            print(deck, perc, count)
        SQLLogDeck(curs, conn, deck, perc)


# Modified range function, because including the actual max you want is handy.
def ranged(x, y):
    return range(x, y + 1)


def generate_decks():
    looping = 1
    localnumcardtypes = numcardtypes
    deck = [c[1] for c in cardtypes]
    decksum = sum(deck)

    while looping:
        if decksum == 60:
            yield list(deck)

        deck[0] += 1
        decksum += 1
        for i in range(localnumcardtypes - 1):
            if deck[i] > cardtypes[i][2]:
                deck[i] = cardtypes[i][1]
                deck[i + 1] += 1
                decksum -= cardtypes[i][2] - cardtypes[i][1]
                if deck[localnumcardtypes - 1] > cardtypes[localnumcardtypes - 1][2]:
                    looping = 0
                    break
            else:
                break


def comb(n, k):
    if k > n:
        return 0
    else:
        if k == n:
            return 1
        else:
            return (factorial(n)) / ((factorial(k)) * (factorial(n - k)))


factorial = Memoize(factorial)
comb = Memoize(comb)


# prob ABNNNNN = (A C copies(A) * B C copies(B) * N C copies(N) over 7 C decksize
def probn(decksize, copies, min_c, max_c, hand):
    n = len(copies)
    denominator = comb(decksize, hand) * 1.0
    res = 0.0
    rem_deck = decksize - sum(copies)
    temp_min = list(min_c)
    looping = 1
    while looping == 1:
        numerator = 1.0
        for i in range(n):
            numerator = numerator * comb(copies[i], temp_min[i])
        numerator = numerator * comb(rem_deck, (hand - sum(temp_min)))
        res = res + (numerator / denominator)
        # looping logic
        if n > 2:
            for j in range(n):
                if (temp_min[j] == max_c[j]) or (sum(temp_min) == hand):
                    temp_min[j] = min_c[j]
                    if j == (n - 1):
                        looping = 0
                else:
                    hand[j] += 1
    # silly special cases cause python is silly
    # omitted cause I'm lazy
    return res


def deckCheck(deck):
    localnumcardtypes = numcardtypes
    mins = [0] * localnumcardtypes
    mins[0] = 1
    hand = list(mins)
    mulled_to = 1
    final = 0
    for h in [7, 6, 5, 4]:
        p = 0
        looping = 1
        while looping == 1:
            # check if hand is 'good'
            for goodhand in goodhands:
                good = 1
                for i in range(localnumcardtypes):
                    if hand[i] < goodhand[i]:
                        good = 0
                        break
                if good == 1:
                    p += probn(sum(deck), deck, hand, hand, h)
                    break
            # looping logic
            for j in range(localnumcardtypes):
                if (hand[j] == deck[j]) or (sum(hand) == h):
                    hand[j] = mins[j]
                    if j == localnumcardtypes - 1:
                        looping = 0
                else:
                    hand[j] += 1
                    break
        final += mulled_to * p
        mulled_to = 1 - final
    return final


def convertStringDeckToArray(deck):
    newdeck = [0] * numcardtypes
    for c in range(len(deck)):
        newdeck[ord(deck[c]) - ord('A')] += 1
    return newdeck


def wipe_out_db():
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    try:
        curs.execute('''DROP TABLE decks''')
        conn.commit()
    except:
        pass
    sql = "CREATE TABLE DECKS ("
    for card in cardtypes:
        sql = ''.join([sql, str(card[0]), " int, "])
    sql = ''.join([sql, "perc float)"])
    curs.execute(sql)
    conn.commit()
    conn.close()


# Check the database for a deck. If it exists, return it.
# Otherwise calculate it and store in DB
def LookupDeck(deck):
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    sql = "SELECT * FROM decks WHERE "
    for i in range(len(deck)):
        if i != 0:
            sql = ''.join([sql, " and "])
        sql = ''.join([sql, str(cardtypes[i][0]), " = ", str(deck[i])])
    curs.execute(sql)
    results = curs.fetchall()
    if results:
        for result in results:
            print(result)
    else:
        perc = deckCheck(deck)
        SQLLogDeck(curs, conn, deck, perc)
        LookupDeck(deck)
    conn.close()


if len(sys.argv) < 2:
    wipe_out_db()

    # Set up the I/O Thread. Necessary because all Sqlite3 stuff should be in same thread
    ioqueue = multiprocessing.queues.SimpleQueue(ctx=multiprocessing.get_context())
    ioprocess = multiprocessing.Process(target=ProcessIO, args=(ioqueue,))
    ioprocess.start()

    pool = multiprocessing.Pool(None, ProcessDeckCheck_init, [ioqueue])

    i = 0
    results = []
    numcpus = multiprocessing.cpu_count()
    #    conn = sqlite3.connect(dbname)
    #    curs = conn.cursor()
    for deck in generate_decks():
        result = pool.apply_async(ProcessDeckCheck, [deck])
        results.append(result)
        i += 1

        if i == numcpus:
            for process in range(numcpus):
                results.pop().get()
            i = 0
            results = []

    for j in range(i):
        results.pop().get()
    pool.close()
    pool.join()
    ioprocess.join()


else:
    deck = []
    if len(sys.argv) == 2:
        deck = convertStringDeckToArray(sys.argv[1])
    else:
        deck = [int(l) for l in sys.argv[1:]]

    LookupDeck(deck)
