
import sys, os, time, signal
import sqlite3, datetime

def sig_handler(signal, frame):

    print "cleaning up before exiting..."
    conn.close()
    sys.exit(0)

if __name__ == '__main__':

    signal.signal(signal.SIGINT, sig_handler)

    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS fermentation_temp
             (date text, temperature real)''')

    # infinite loop to do stuff
    while True:

        # TODO: use sysfs interface for 1-wire thermometer
        print "reading temperature :"
        temp_fd = open("data.txt", 'r')
        temp_fd.close()

        # TODO: save real temperature
        c.execute("INSERT INTO fermentation_temp VALUES (?, ?)", (datetime.datetime.now(), 23))
        c.execute("SELECT * FROM fermentation_temp")
        for data in c.fetchall():
            print data

        conn.commit()
        time.sleep(30)
