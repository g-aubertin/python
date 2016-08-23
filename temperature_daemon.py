
import sys, os, time, signal
import sqlite3, datetime



def dump_db():

    conn = sqlite3.connect('beer_machine.db')
    c = conn.cursor()
    c.execute("SELECT * FROM fermentation_temp")
    for data in c.fetchall():
        print data

def sig_handler(signal, frame):

    print "cleaning up before exiting..."
    dump_db()
    conn.close()
    sys.exit(0)

if __name__ == '__main__':

    signal.signal(signal.SIGINT, sig_handler)

    # database init
    conn = sqlite3.connect('beer_machine.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS fermentation_temp
             (date text, temperature float)''')
    conn.close()

    # infinite loop to do stuff
    while True:

        # read file from 1-wire sysfs and extract temperature
        fd = open("/sys/bus/w1/devices/28-031600cde1ff/w1_slave", "r")
        temp_str = fd.read()
        fd.close()
        temp_str = temp_str.split()
        temp_str = temp_str[-1].translate(None, " t=")
        temp = float(temp_str) / 1000
        print "current temperature :", temp

        # store in db
        conn = sqlite3.connect('beer_machine.db')
        c = conn.cursor()
        c.execute("INSERT INTO fermentation_temp VALUES (?, ?)", (datetime.datetime.now(), temp))
        conn.commit()
        conn.close()

        time.sleep(30)
