# SmartKart
An RFID based billing system with a NodEMCU and RFID reader.
![app](https://user-images.githubusercontent.com/59250093/145529378-4ccd853f-f51f-4b29-8d91-f34b69e337be.jpeg)
![img](https://user-images.githubusercontent.com/59250093/147275682-711cda60-68de-4af9-9c4d-e8c4a9695023.jpg)
![img2](https://user-images.githubusercontent.com/59250093/147275755-455584c0-8d90-4cd8-baf6-3916f89595cf.jpg)

# Setup and Usage
- First set up the rfid database using the db_setup.py script within
sqlite_scripts.
- Use `python3 sqlite_scripts/db_setup.py`.
- Then run the flask app with `python3 app.py`.
- Change the url in read.py to your flask url.
- Now you must load the read.py and mfrc522.py within the esp directory,
onto your esp8266 wired up as shown in the pictures above.
- Then navigate into your esp’s repl, and do `from read import do_read`.
- Then execute `do_read()`.(See screenshot below for execution)
- Now if you have wired your circuit correctly, pressing the bottom button
should allow you to scan an item, and add it into your bill. (to see the bill
navigate to http://FLASK_URL/bill?uid=1.
- Similarly the other button will allow you to delete items from the bill.
