all: deck12.sqlite3 deck13.sqlite3 deck14.sqlite3

clean:
	rm -rf *sqlite3 *~ *journal

deck12.sqlite3: findthebestdeck.py
	python findthebestdeck.py 12

deck13.sqlite3: findthebestdeck.py
	python findthebestdeck.py 13

deck14.sqlite3: findthebestdeck.py
	python findthebestdeck.py 14
