import mfrc522
from os import uname
import urequests as requests
import time
import machine

def do_read():

    if uname()[0] == 'WiPy':
        rdr = mfrc522.MFRC522("GP14", "GP16", "GP15", "GP22", "GP17")
    elif uname()[0] == 'esp8266':
        rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
    else:
        raise RuntimeError("Unsupported platform")

    deletebut = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
    addbut = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)

    pressed = False
    url = ''

    try:
        while True:
            if not pressed:
                print("")
                print("Please press either add or delete button to continue")
                print("")

                while not pressed:
                    if deletebut.value() == 0:
                        print("delete button pressed")
                        url = 'http://192.168.29.236:5000/delete'
                        pressed = True
                    elif addbut.value() == 0:
                        print("add button pressed")
                        url = 'http://192.168.29.236:5000/add'
                        pressed = True
                    else:
                        time.sleep_ms(10)

                print("")
                print("Place card before reader to read from address 0x08")
                print("")


            (stat, tag_type) = rdr.request(rdr.REQIDL)

            if stat == rdr.OK:
                (stat, raw_uid) = rdr.anticoll()

                if stat == rdr.OK:
                    print("New card detected")
                    print("  - tag type: 0x%02x" % tag_type)
                    print("  - uid	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print("")

                    if rdr.select_tag(raw_uid) == rdr.OK:
                            key = [255, 255, 255, 255, 255, 255]
                            if rdr.auth(rdr.AUTHENT1B, 8, key, raw_uid) == rdr.OK:
                                data = "".join([str(x) for x in rdr.read(8)])
                                rdr.stop_crypto1()
                                print("Address 8 data: %s" % data)
                                print(url + '?uid=1&rfid=' + data)
                                requests.get(url + '?uid=1&rfid=' + data)
                                pressed = False
                            else:
                                print(keyhex + " is not the key")
                    else:
                        print("Failed to select tag")

    except KeyboardInterrupt:
            print("Bye")
