#!/usr/bin/env python3
import sqlite3
import os.path

filename = '../rfid_db.db'

if os.path.isfile(filename):
    dbexists = True
else:
    dbexists = False

con = sqlite3.connect(filename)
cur = con.cursor()

if not dbexists:
    cur.execute('''CREATE TABLE rfids (
        id VARCHAR(40) NOT NULL UNIQUE,
        item VARCHAR(30) NOT NULL UNIQUE,
        price INTEGER NOT NULL
    )''')
    rfids = [
        ('1123456789101112131415', 'banana', 50),
        ('713248511008409899100101102103104105', 'chocopie', 10),
        ('6578246924084015999100101102103104105', 'apple', 40),
        ('681841781798409899100101102103104105', 'cake', 70),
        ('6325212825219140402310000000', 'detergent', 30),
        ('0000000000000000', 'toothbrush', 20)
    ]
    cur.executemany("INSERT INTO rfids VALUES (?, ?, ?)", rfids)
else:
    print('DB already exists')

for row in cur.execute("SELECT * FROM rfids").fetchall():
    print(row)
con.commit()
con.close()
