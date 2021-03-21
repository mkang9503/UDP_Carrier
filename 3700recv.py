#!/usr/bin/python -u
#
# CS3700, Spring 2015
# Project 2 Starter Code
#

import sys
import socket
import time
import datetime
import select
import json
import struct


def log(string):
    sys.stderr.write(datetime.datetime.now().strftime("%H:%M:%S.%f") + " " + string + "\n")


# insert element sorted by sequence, x is a tuple (data, sequence)
def insert_array(array, x):
    for i in range(len(array)):
        if array[i][1] > x[1]:
            return array[:i] + [x] + array[i:]
    return array + [x]


MSG_SIZE = 1500
TIMEOUT = 30

# Bind to localhost and an ephemeral port
UDP_IP = "127.0.0.1"
UDP_PORT = int(sys.argv[1])
# UDP_PORT = 0

# Set up the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(TIMEOUT)

# Get port we bound to
UDP_PORT = sock.getsockname()[1]
log("[bound] " + str(UDP_PORT))

packets_recv = []

# Now listen for packets
while True:
    try:
        result = sock.recvfrom(MSG_SIZE)  # causes TIMEOUT ERROR

        # If nothing is ready, we hit the timeout
        if result:
            (data, addr) = result

            try:
                decoded = data
                seq, d, ack, eof = struct.unpack('i{}si?'.format(len(data) - 9), decoded)
                # log("SEQ: " + str(seq))
                # d = d.decode('utf-8')
                # log("D: " + d)
                # log("ACK: " + str(ack))
                # If the EOF flag is set, exit
                if eof:
                    # print data of packets
                    for p in packets_recv:
                        sys.stdout.write(p[0])
                    log("[completed]")
                    sys.exit(0)

                # If there is data, we accept it and print it out
                if d:
                    # If we receive data, we assume it's in-order
                    # You will need to do much more here
                    sequence = seq
                    log("STR Length: " + str(len(packets_recv)))
                    if (d, sequence) not in packets_recv:
                        log("[recv data] " + str(seq) + " (" + str(
                            len(d)) + ") ACCEPTED (in-order)")
                        packets_recv = insert_array(packets_recv, (d, sequence))

                # Send back an ack to the sender
                msg = struct.pack('i{}si?'.format(0), seq, "", seq + len(d), False)
                # {"ack": decoded['sequence'] + len(decoded['data'])})
                # int, string, int, bool
                # seq, data, ack, eof
                log("ABOUT TO SEND " + msg)
                if sock.sendto(msg, addr) < len(msg):
                    log("[error] unable to fully send packet")

            except (ValueError, KeyError, TypeError) as e:
                log("[recv corrupt packet]")
                raise e
        else:
            log("[error] timeout")
            sys.exit(-1)
    except socket.timeout:
        # server did not get ACK, resend last packet?
        log('RECV: TIMEOUT ERROR')
