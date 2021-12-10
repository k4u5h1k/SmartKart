#!/usr/bin/env python3
import os
import sqlite3

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

filename = 'rfid_db.db'
con = sqlite3.connect(filename, check_same_thread=False)
cur = con.cursor()

data = []

def getproduct(rfid, cur):
    results = cur.execute("SELECT item, price FROM rfids WHERE id=:rfid", {'rfid': rfid}).fetchall()
    
    item, price = -1, -1
    if len(results)==1:
        item, price = results[0]

    return item, price

@app.route('/',methods=['GET'])
def index():
    global data
    return render_template('index.html',data = data)

@app.route('/add',methods=['GET'])
def add():
    global data

    # user [id, item, price, quantity]
    user = []
    user.append(request.args.get('uid'))
    rfid = request.args.get('rfid')

    cur = con.cursor()
    item, price = getproduct(rfid, cur)
    user.extend([item, price])

    if user.count(-1)>0 or user.count(None)>0 or len(user)<3:
        print('Insufficient items')
        return render_template('index.html',data = data)

    for index,row in enumerate(data):
        if row[:-1] == user:
            data[index][-1] += 1
            break
    else:
        data.append(user + [1])

    return render_template('index.html',data = data)

@app.route('/delete',methods=['GET'])
def delete():
    global data
    todelete = []
    todelete.append(request.args.get('uid'))
    rfid = request.args.get('rfid')

    item, price = getproduct(rfid, cur)

    todelete.extend([item, price])

    for index,row in enumerate(data):
        if row[:-1] == todelete:
            if data[index][-1]>1:
                data[index][-1]-=1
            else:
                data.pop(index)    

    return render_template('index.html',data = data)

@app.route('/bill',methods=['GET'])
def total():
    global data
    user = request.args.get('uid')
    total = 0
    bill = []

    for index,row in enumerate(data):
        if row[0] == user:
            bill.append(row[1:])
            total += row[2]*row[3]

    return render_template('bill.html',data=bill, total=total)

@app.route('/paid',methods=['GET'])
def paid():
    global data

    user = request.args.get('id')
    for index,row in reversed(list(enumerate(data))):
        if row[0] == user:
            data.pop(index)

    return render_template('index.html',data = data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
