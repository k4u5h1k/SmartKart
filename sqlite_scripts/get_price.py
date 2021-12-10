#!/usr/bin/env python3
import sqlite3

filename = 'rfid_db.db'
con = sqlite3.connect(filename)
cur = con.cursor()

def getproduct(rfid, cur):

    results = cur.execute("SELECT item, price FROM rfids WHERE id=:rfid", {'rfid': rfid}).fetchall()
    
    item, price = -1, -1
    if len(results)==1:
        item, price = results[0]

    return item, price

print(getprice('6325212825219140402310000000', cur))
