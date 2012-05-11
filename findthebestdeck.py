import time
import os
import sys
import sqlite3
import multiprocessing #import Pool, Process, Queue
from math import factorial 

# Globals
cardtypes = []
goodhands = []
lock = multiprocessing.Lock()

# Run-time constants
dbname = 'rainbow.sqlite3'
dredge_configuration = 1

# Set up the set of cards we could use
# ["Card Name", Min, Max]
if dredge_configuration == 0:
	dbname = "rainbow.sqlite3"
	cardtypes = [
		["Dredger", 8, 12],
		["Faithless_Looting", 0, 4],
		["Lion_s_Eye Diamond", 0, 4],
		["Putrid_Imp_Cabal_Therapy_Tireless Tribe", 2, 12],
		["Careful_Study_Hapless_Researcher", 0, 8],
		["Breakthrough", 0, 4],
		["Winds_of_Change", 0, 4],
		["Cephalid_Coliseum", 0, 4],
		["Rainbow_Land", 8, 16],
		["Win_Condition", 12, 15]]

	#goodhands = ["AABC", "ABCI", "ACEI", "ACFI", "ABDI", "ADEI", "ADFI", "ADHI", "ABBI", "ABEI", "ABFI", "ABHI", "ABEI", "AEEI", "AEFI", "AEHI", "AEHH", "AEEH", "AEFH", "ABGI", "ADGI", "AEGI"]
	goodhands = [[2, 1, 1, 0, 0, 0, 0, 0, 0, 0],
		[1, 1, 1, 0, 0, 0, 0, 0, 1, 0],
		[1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
		[1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
		[1, 1, 0, 1, 0, 0, 0, 0, 1, 0],
		[1, 0, 0, 1, 1, 0, 0, 0, 1, 0],
		[1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
		[1, 0, 0, 1, 0, 0, 0, 1, 1, 0],
		[1, 2, 0, 0, 0, 0, 0, 0, 1, 0],
		[1, 1, 0, 0, 1, 0, 0, 0, 1, 0],
		[1, 1, 0, 0, 0, 1, 0, 0, 1, 0],
		[1, 1, 0, 0, 0, 0, 0, 1, 1, 0],
		[1, 1, 0, 0, 1, 0, 0, 0, 1, 0],
		[1, 0, 0, 0, 2, 0, 0, 0, 1, 0],
		[1, 0, 0, 0, 1, 1, 0, 0, 1, 0],
		[1, 0, 0, 0, 1, 0, 0, 1, 1, 0],
		[1, 0, 0, 0, 1, 0, 0, 2, 0, 0],
		[1, 0, 0, 0, 2, 0, 0, 1, 0, 0],
		[1, 0, 0, 0, 1, 1, 0, 1, 0, 0],
		[1, 1, 0, 0, 0, 0, 1, 0, 1, 0],
		[1, 0, 0, 1, 0, 0, 1, 0, 1, 0],
		[1, 0, 0, 0, 1, 0, 1, 0, 1, 0]]


elif dredge_configuration == 1:
	dbname = "mckeown.sqlite3"
	cardtypes = [
		["Dredger", 8, 12],
		["Faithless_Looting", 0, 4],
		["Lion_s_Eye_Diamond", 0, 4],
		["Putrid_Imp_Cabal_Therapy", 2, 8],
		["Careful_Study_Hapless_Researcher", 0, 8],
		["Breakthrough", 0, 4],
		["Winds_of_Change", 0, 4],
		["Cephalid_Coliseum", 0, 4],
		["Fetchland", 0, 8],
		["Volcanic_Island", 1, 4],
		["Bayou", 1, 4],
		["Win_Condition", 12, 17]]

	goodhands = [
		[2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0], [2, 1, 2, 0, 1, 0, 0, 0, 1, 1, 0, 0],
		[1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0], [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0], [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
		[1, 0, 0, 1, 0, 0, 1, 0, 2, 0, 0, 0], [1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0], [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0],
		[1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0], [1, 1, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0], [1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0],
		[1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0], [1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0], [1, 0, 0, 1, 1, 0, 0, 0, 2, 0, 0, 0],
		[1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0], [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0], [1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
		[1, 0, 0, 1, 0, 1, 0, 0, 2, 0, 0, 0], [1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0], [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
		[1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0], [1, 0, 0, 1, 0, 0, 0, 1, 2, 0, 0, 0], [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0],
		[1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0], [1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0], [1, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
		[1, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], [1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
		[1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0], [1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0], [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
		[1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0], [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], [1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
		[1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0], [1, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0], [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
		[1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0], [1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0], [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
		[1, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0], [1, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
		[1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0], [1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0], [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
		[1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0]]

		#goodhands = ["AABC", "ABCI", "ABCJ" "ACEI", "ACEJ", "ACFI", "ACFJ", "ADGII","ADGIJ", "ADGIK", "ADGJK", "ABDII", "ABDIJ", "ABDIK", "ABDJK", "ADEII", "ADEIJ", "ADEIK", "ADEJK", "ADFII", "ADFIJ", "ADFIK", "ADFJK", "ADHII", "ADHIJ", "ADHIK", "ADHJK", "ABBI", "ABBJ", "ABEI", "ABEJ", "ABFI", "ABFJ", "ABHI", "ABHJ", "ABEI", "ABEJ", "AEEI", "AEEJ", "AEFI", "AEFJ", "AEHI", "AEHJ", "AEHH", "AEEH", "AEFH", "ABGI", "ABGJ", "AEGI", "AEGJ"]

elif dredge_configuration == 2:
	dbname = "mckeown2.sqlite3"
	cardtypes = [
		["Dredger", 8, 12],
		["Faithless_Looting", 0, 4],
		["Lion_s_Eye_Diamond", 0, 4],
		["Putrid_Imp_Cabal_Therapy", 2, 8],
		["Careful_Study_Hapless_Researcher", 0, 8],
		["Breakthrough", 0, 4],
		["Winds_of_Change", 0, 4],
		["Cephalid_Coliseum", 0, 4],
		["Fetchland", 0, 8],
		["Volcanic_Island", 1, 4],
		["Bayou", 0, 0],
		["Win_Condition", 12, 17]]

	goodhands = [
		[2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0], [2, 1, 2, 0, 1, 0, 0, 0, 1, 1, 0, 0],
		[1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0], [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0], [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
		[1, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
		[1, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], [1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
		[1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0], [1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0], [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
		[1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0], [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], [1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
		[1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0], [1, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0], [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
		[1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0], [1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0], [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
		[1, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0], [1, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
		[1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0], [1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0], [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
		[1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0]]

class Memoize: # stolen from http://code.activestate.com/recipes/52201/
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
	for card in xrange(len(deck)):
		sql = ''.join([sql, str(deck[card]) + ", "])
	sql = ''.join([sql, str(perc) + ")"])
	cursor.execute(sql)
	connection.commit()

def ProcessDeckCheck(deck):
	perc = deckCheck(deck)
	ProcessDeckCheck.ioqueue.put([deck, perc])

def ProcessDeckCheck_init(ioqueue):
	ProcessDeckCheck.ioqueue = ioqueue

def ProcessDecks(ioqueue,lock):
	lock.acquire()
	for deck in generatedecks():
		lock.release()
		deck = ioqueue.get()
		perc = deckCheck(deck)
		ioqueue.put_nowait([deck, perc])
		lock.acquire()
	print("Done processing")

def ProcessIO(ioqueue):
	conn = sqlite3.connect(dbname)
	curs = conn.cursor()

	count = 0
	bestperc = 0.0

	while 1:
		if ioqueue.empty():
			time.sleep(10)
			if count == 0:
				continue
			if ioqueue.empty():
				print("Completed ",count," decks")
				return count
		temp = ioqueue.get(True)
		count += 1
		deck = temp[0]
		perc = temp[1]
		if perc > bestperc:
			bestperc = perc
			print(deck, perc, count)
		SQLLogDeck(curs, conn, deck, perc)

# Modified xrange function, because including the actual max you want is handy.
def ranged(x, y):
	return xrange(x, y + 1)

def generatedecks():
	looping = 1
	deck = [c[1] for c in cardtypes]
	
	while looping:
		if sum(deck) == 60:
			yield list(deck) 
		
		deck[0] += 1
		for i in xrange(len(cardtypes) - 1):
			if deck[i] > cardtypes[i][2]:
				deck[i] = cardtypes[i][1]
				deck[i+1] += 1
				if deck[len(cardtypes)-1] > cardtypes[len(cardtypes)-1][2]:
					looping = 0
					break
			else:
				break

def comb(n, k):
	if (k > n):
		return 0
	else:
		if (k == n):
			return 1
		else:
			return ((factorial(n))/((factorial(k))*(factorial(n-k))))

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
		for i in xrange(n):
			numerator = numerator * comb(copies[i],tempMin[i])
		numerator = numerator * comb(remDeck,(hand - sum(tempMin)))
		res = res + (numerator/denominator)
		#looping logic
		if(n > 2):
			for j in xrange(n):
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
	mins = [0] * len(cardtypes)
	mins[0] = 1
	hand = list(mins)
	mulledTo = 1
	final = 0
	for h in [7, 6, 5, 4]:
		p = 0
		looping = 1
		while(looping == 1):
			#check if hand is 'good'
			for goodhand in goodhands:
				good = 1
				for i in xrange(len(cardtypes)):
					if (hand[i] < goodhand[i]):
						good = 0
						break
				if (good == 1):
					p = p + probn(sum(deck),deck,hand,hand,h)
					break
			#looping logic
			for j in xrange(len(cardtypes)):
				if ((hand[j] == deck[j]) or (sum(hand) == h)):
						hand[j] = mins[j]
						if(j == len(cardtypes)-1):
							looping = 0
				else:
					hand[j] += 1
					break
		final = final + mulledTo * p
		mulledTo = 1 - final
	return final

def convertStringDeckToArray(deck):
	newdeck = [0] * len(cardtypes)
	for c in xrange(len(deck)):
		newdeck[ord(deck[c])-ord('A')] += 1
	return newdeck

def convertArrayDeckToString(listofints):
	deck = ""
	for c in xrange(len(listofints)):
		deck += string.uppercase[c]*int(listofints[c])
	return deck

def WipeoutDB():
	conn = sqlite3.connect(dbname)
	curs = conn.cursor()
	try:
		curs.execute('''DROP TABLE decks''')
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
	for i in xrange(len(deck)):
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
	WipeoutDB()

	# Set up the I/O Thread. Necessary because all Sqlite3 stuff should be in same thread
	ioqueue = multiprocessing.Queue()
	ioprocess = multiprocessing.Process(target=ProcessIO, args=(ioqueue,))
	ioprocess.start()

	#for i in xrange(multiprocessing.cpu_count()):
	#	deckprocess = multiprocessing.Process(target=ProcessDecks, args=(ioqueue,lock,))

	pool = multiprocessing.Pool(None, ProcessDeckCheck_init, [ioqueue])

	i = 0
	results = []
	for deck in generatedecks():

		result = pool.apply_async(ProcessDeckCheck, [deck])
		results.append(result)
		i += 1

		if i == multiprocessing.cpu_count():
			for process in xrange(multiprocessing.cpu_count()):
				results[process].get()
			i = 0
			results = []

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
