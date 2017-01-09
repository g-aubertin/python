#!/usr/bin/python

import sys
import re
import csv

# function definitions
###########################
def sdio_cmd_parser(filename, start_trace, end_trace):

    latency_table = []
    couple_values = 0
    start_found = 0
    measures = 0
    trace_file = open(filename, "r")

    with trace_file as fp:
        for line in fp:

            # find start
            if start_trace in line:
                toto = re.sub( ' +', ' ',line)
                toto  = toto.split(" ")
                start_timing = float(toto[3][:-1])
                start_found = 1

            # find end
            if end_trace in line:
                if start_found == 1:
                    titi = re.sub( ' +', ' ',line)
                    titi  = titi.split(" ")
                    stop_timing = float(titi[3][:-1])
                    couple_values = 1

            # calculate latency and store in the array
            if couple_values == 1:
                latency = stop_timing - start_timing
                latency_table.append(latency * 100000)
                measures = measures + 1
                couple_values = 0
                start_found = 0

    return latency_table

def sdio_cmd_parser_graph(filename, start_trace, end_trace):

    latency_table = []
    couple_values = 0
    start_found = 0
    measures = 0
    trace_file = open(filename, "r")


    with trace_file as fp:
        for line in fp:

            # find start
            if start_trace in line:
                start_found = 1

            if end_trace in line:
                if start_found == 1:
                    titi = re.sub( ' +', ' ',line)
                    titi  = titi.split(" ")
                    latency = float(titi[3][:-1])
                    couple_values = 1

            # calculate latency and store in the array
            if couple_values == 1:
                latency_table.append(latency)
                measures = measures + 1
                couple_values = 0
                start_found = 0

    return latency_table


def print_cmd_statistics(table):


    print "number of commands :", len(table)
    if (len(table) > 0):
        print "CMD average timing : ", ((sum(table) / len(table))), "us"
        print "CMD median timing : ", median(table), "us"
        print "CMD 90th percentile : ", percentile(table, 90), "us"
        print "CMD min timing : ", min(table), "us"
        print "CMD max timing : ", max(table), "us"
    print ""

def csv_export_timings(table):
    myfile = open("table.csv", 'wb')
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(table)


def median(mylist):
    mylist = sorted(mylist)
    if len(mylist) == 0:
        return none;
    if len(mylist) %2 == 1:
            return mylist[((len(mylist)+1)/2)-1]
    else:
            return float(sum(mylist[(len(mylist)/2)-1:(len(mylist)/2)+1]))/2.0

def percentile(mylist, percent):
    mylist = sorted(mylist)
    if len(mylist) == 0:
        return none;
    index = int(len(mylist) / 100 * percent)
    return mylist[index]

# main
###########################

print "trace file is : ", sys.argv[1]
print ""
print "========================"
print "statistics for CMD52"
print "========================"
print_cmd_statistics(sdio_cmd_parser(sys.argv[1], "mmc2: starting CMD52", "mmc2: req done (CMD52)"))
print "========================"
print "statistics for CMD53 - 32 Kbytes read"
print "========================"
print_cmd_statistics(sdio_cmd_parser(sys.argv[1], "CMD53 arg 18000040", "mmc2:     32768 bytes"))
print "========================"
print "statistics for CMD53 - 16 Kbytes read"
print "========================"
print_cmd_statistics(sdio_cmd_parser(sys.argv[1], "CMD53 arg 18000020", "mmc2:     16384 bytes"))
print "========================"
print "statistics for CMD53 - 32 Kbytes write"
print "========================"
print_cmd_statistics(sdio_cmd_parser(sys.argv[1], "CMD53 arg 98000040", "mmc2:     32768 bytes"))
print "========================"
print "statistics for CMD53 - 31 Kbytes write"
print "========================"
print_cmd_statistics(sdio_cmd_parser(sys.argv[1], "CMD53 arg 9800003d", "mmc2:     31232 bytes"))
print "========================"
print "statistics for CMD53 - 16 Kbytes write"
print "========================"
print_cmd_statistics(sdio_cmd_parser(sys.argv[1], "CMD53 arg 98000022", "mmc2:     17408 bytes"))


print ""
print "stats for sdio_readb() :"
print_cmd_statistics(sdio_cmd_parser_graph(sys.argv[1], "sdio_readb()", "}"))
print "stats for sdio_readsb() :"
print_cmd_statistics(sdio_cmd_parser_graph(sys.argv[1], "sdio_readsb()", "}"))
print "stats for sdio_writeb() :"
print_cmd_statistics(sdio_cmd_parser_graph(sys.argv[1], "sdio_writeb()", "}"))
print "stats for sdio_writesb() :"
print_cmd_statistics(sdio_cmd_parser_graph(sys.argv[1], "sdio_writesb()", "}"))
