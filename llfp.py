#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
llfp by James Gill - A Lutron LEAP Python library
Contributions by Timothy Gill
https://github.com/JJTech0130/LLFP

'''

import json
import leapjson
import socket
import ssl
import sys
if sys.version_info[0] > 2:
    PY3K = True
else:
    PY3K = False

#Don't change this, declare it with bridge obj.
DEBUG = False

def parseStatusCode(jsontoparse):
    if DEBUG == True: print(jsontoparse)
    jsontoparse = jsontoparse.decode('utf-8')
    jsontoparse = json.loads(jsontoparse)
    StatusCode = jsontoparse["Header"]["StatusCode"]
    if StatusCode == "200 OK" && DEBUG == False:
        return
    else:
        return StatusCode
class bridge:
    def __init__(self, host, port=8085, debug=False):
        global DEBUG
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        self.wrappedSocket = ssl.wrap_socket(sock)
        self.wrappedSocket.connect((host,port))
        DEBUG = debug
    def ping(self):
        self.wrappedSocket.send(leapjson.pingPacket.encode('utf-8'))
        return parseStatusCode(self.wrappedSocket.recv())
    def login(self, loginId, password):
        packet = leapjson.loginPacket % (loginId, password)
        packet = packet.encode('utf-8')
        self.wrappedSocket.send(packet)
        return parseStatusCode(self.wrappedSocket.recv())
class zone():
    def __init__(self, zoneId, bridgeobj):
        global DEBUG
        self.zoneId = zoneId
        self.wrappedSocket = bridgeobj.wrappedSocket

    def goToLevel(self, level, fadeTime="00:00:05", delayTime="00:00:00"):
        packet = leapjson.goToLevelPacket % (self.zoneId, level, fadeTime, delayTime)
        packet = packet.encode('utf-8')
        self.wrappedSocket.send(packet)
        return parseStatusCode(self.wrappedSocket.recv())

if __name__ == __main__:
    print("This is a library, and is NOT meant to run standalone.")
    print("(But you can try some examples to see how it works!)")
