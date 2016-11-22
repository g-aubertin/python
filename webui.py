#!/usr/bin/python

import os, sys, sqlite3

def print_db(connection, index):

    c = connection.cursor()
    c.execute("SELECT * from fermentation_temp")
    data = c.fetchall()
    for line in data:
        index.write( "['" + str(line[0])+ "', " + str(line[1]) + "], \n")

def refresh(connection):

    index = open('/opt/beer_machine/index.html', 'w')

    fd_template = open("/opt/beer_machine/web/template.html")
    html_template = fd_template.read().splitlines()
    for line in html_template:
        index.write(line + "\n")

    print_db(connection, index)

    fd_template = open("/opt/beer_machine/web/template_end.html")
    html_template = fd_template.read().splitlines()
    for line in html_template:
        index.write(line + "\n")

    index.close()
