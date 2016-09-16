#!/usr/bin/env python

import sys, os, time, signal
import sqlite3, datetime
import webui

SOCKET_CODE_ON = 0
SOCKET_CODE_OFF = 0
W1_PATH = ""
DURATION = 0
TEMP = 0
NAME = ""

def get_config(path):

    global W1_PATH, SOCKET_CODE_ON, SOCKET_CODE_OFF
    fd_config = open(path, 'r')
    for line in fd_config.readlines():
        line = " ".join(line.split())
        line = line.split(" ")
        if (line[0] == "W1_PATH"):
            print "W1_PATH :", line[1]
            W1_PATH = line[1]
        if (line[0] == "SOCKET_CODE_ON"):
            print "SOCKET_CODE_ON :", line[1]
            SOCKET_CODE_ON = int(line[1])
        if (line[0] == "SOCKET_CODE_OFF"):
            print "SOCKET_CODE_OFF :", line[1]
            SOCKET_CODE_OFF = int(line[1])
        if (line[0] == "DURATION"):
            print "DURATION :", line[1]
            DURATION = int(line[1])
        if (line[0] == "TEMP"):
            print "TEMP :", line[1]
            TEMP = int(line[1])
        if (line[0] == "NAME"):
            print "NAME :", line[1]
            NAME = int(line[1])
    fd_config.close()

def read_temperature():

    # read file from 1-wire sysfs and parse result
    fd = open(W1_PATH, "r")
    temp_str = fd.read()
    fd.close()
    temp_str = temp_str.split()
    temp_str = temp_str[-1].translate(None, " t=")
    temp_flt = float(temp_str) / 1000
    print "current temperature :", temp_flt
    return temp_flt

def socket_command(value):

    cmd = "RFSource/codesend %d" % value
    os.system(cmd)
    if value == SOCKET_CODE_ON:
        return 1
    else:
        return 0

def dump_db():

    conn = sqlite3.connect('beer_machine.db')
    c = conn.cursor()
    c.execute("SELECT * FROM fermentation_temp")
    for data in c.fetchall():
        print data

if __name__ == '__main__':

    if (len(sys.argv) < 2):
        print "configuration file needed"
        sys.exit(0)

    # check if 433Mhz tools are compiled
    if os.path.exists("RFSource/codesend") == False:
        print "433Mhz tools are not compiled. exiting.."
        sys.exit(0)

    # read configuration file and set variables
    get_config(sys.argv[1])

    # database init
    conn = sqlite3.connect('beer_machine.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS fermentation_temp
             (date text, temperature float, switch int)''')
    conn.close()

    # before getting started, we switch off the plug to be in a known state
    socket_status = socket_command(SOCKET_CODE_OFF);

    # infinite loop to do stuff
    while True:

        # get temperature
        temp = read_temperature()

        # store in db
        conn = sqlite3.connect('beer_machine.db')
        c = conn.cursor()
        c.execute("INSERT INTO fermentation_temp VALUES (?, ?, ?)", (datetime.datetime.now(), temp,
                                                                     socket_status))
        conn.commit()

        # refresh web page
        webui.refresh(conn)
        conn.close()

        # adjust temperature with socket
        # TODO: use pid
        if temp > 20.5:
            socket_status = socket_command(SOCKET_CODE_ON);
        if temp < 20:
            socket_status = socket_command(SOCKET_CODE_OFF);

        time.sleep(30)
