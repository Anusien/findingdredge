all: deck12.sqlite3 deck13.sqlite3 deck14.sqlite3 deck15.sqlite3

clean:
	rm -rf *sqlite3 *~ *journal

deck12.sqlite3: findthebestdeck.py
	python -u findthebestdeck.py 12|python -u feedto.py deck12.sqlite3

deck13.sqlite3: findthebestdeck.py
	python -u findthebestdeck.py 13|python -u feedto.py deck13.sqlite3

deck14.sqlite3: findthebestdeck.py
	python -u findthebestdeck.py 14|python -u feedto.py deck14.sqlite3

deck15.sqlite3: findthebestdeck.py
	python -u findthebestdeck.py 15|python -u feedto.py deck15.sqlite3
