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

MSG_SIZE = 1500
DATA_SIZE = 1000
TIMEOUT = 30
SEQUENCE = 0

# Bind to localhost and an ephemeral port
IP_PORT = sys.argv[1]
UDP_IP = IP_PORT[0:IP_PORT.find(":")]
UDP_PORT = int(IP_PORT[IP_PORT.find(":") + 1:])
dest = (UDP_IP, UDP_PORT)
start = time.time()
prevRTT = 0.5
sumRTT = 0.0

# Set up the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIMEOUT)


def log(string):
    sys.stderr.write(datetime.datetime.now().strftime("%H:%M:%S.%f") + " " + string + "\n")


packets_sent = []


def send_next_packet():
    global SEQUENCE

    data = sys.stdin.read(DATA_SIZE)  # causing time our error??
    if len(data) > 0:
        msg = struct.pack('i{}si?'.format(len(data)), SEQUENCE, data.encode('utf-8'), False, False)
        SEQUENCE += len(data)

        if sock.sendto(msg, dest) < len(msg):
            log("[error] unable to fully send packet")
        else:
            log("[send data] " + str(SEQUENCE) + " (" + str(len(data)) + ")")
            packets_sent.append(msg)
        return True
    else:
        return False


# Send first packet
send_next_packet()

# Now read in data, send packets
while True:
    log("ABOUT TO SLEEP")
    try:

        result = sock.recvfrom(MSG_SIZE)  # <= causes time out
        rtt = time.time() - start
        sumRTT = sumRTT+rtt
        log('RTT: ' + str(rtt))
        start = time.time()
        log('START: ' + str(start))
        x = sumRTT/len(packets_sent) if len(packets_sent) > 0.0 else 1.0
        log(str(x))
        if rtt > (x*2.0):
            # log(x)
            # packet lost, resend previous packet
            sock.sendto(packets_sent[-1], dest)

            continue

        if result:

            (data, addr) = result
            try:
                decoded = data
                sequence, data, ack, eof = struct.unpack('i{}si?'.format(len(data) - 9), decoded)

                # If there is an ack, send next packet
                if ack == SEQUENCE:
                    log("[recv ack] " + str(SEQUENCE))

                    # Try to send next packet; break if no more data
                    if not send_next_packet():
                        break
                # else:
                #     sock.sendto(packets_sent[-1], dest)
            except (ValueError, KeyError, TypeError):
                log("[recv corrupt packet]")
        else:
            log("[error] timeout")
            sys.exit(-1)
    except socket.timeout:
        # server did not get ACK, resend last packet?
        log('TIMEOUT ERROR')

# {"sequence": SEQUENCE, "data": "", "ack": False, "eof": True, }
sock.sendto(struct.pack('i{}si?'.format(0), SEQUENCE, "", 0, True), dest)
sys.exit(0)
