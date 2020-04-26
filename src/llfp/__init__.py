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

DEBUG = False

def parseStatusCode(jsontoparse):
    '''
    Parse the JSON status codes retured
    '''
    if DEBUG == True: print(jsontoparse)
    jsontoparse = jsontoparse.decode('utf-8')
    jsontoparse = json.loads(jsontoparse)
    StatusCode = jsontoparse["Header"]["StatusCode"]
    if StatusCode == "200 OK" and DEBUG == False:
        return
    else:
        return StatusCode
class bridge:
    '''
    Control the bridge/processor
    '''
    def __init__(self, host, port=8085):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        self.wrappedSocket = ssl.wrap_socket(sock)
        self.wrappedSocket.connect((host,port))
    def ping(self):
        self.wrappedSocket.send(leapjson.pingPacket.encode('utf-8'))
        return parseStatusCode(self.wrappedSocket.recv())
    def login(self, loginId, password):
        packet = leapjson.loginPacket % (loginId, password)
        packet = packet.encode('utf-8')
        self.wrappedSocket.send(packet)
        return parseStatusCode(self.wrappedSocket.recv())
class zone():
    '''
    Control zones
    '''
    def __init__(self, zoneId, bridgeobj):
        self.zoneId = zoneId
        self.wrappedSocket = bridgeobj.wrappedSocket

    def goToLevel(self, level, fadeTime="00:00:05", delayTime="00:00:00"):
        packet = leapjson.goToLevelPacket % (self.zoneId, level, fadeTime, delayTime)
        packet = packet.encode('utf-8')
        self.wrappedSocket.send(packet)
        return parseStatusCode(self.wrappedSocket.recv())
    def goToColor(self, level, hue, fadeTime="00:00:05", delayTime="00:00:00"):
        packet = leapjson.goToColorPacket % (self.zoneId, level, 50, hue, 100, delayTime, fadeTime)
        packet = packet.encode('utf-8')
        self.wrappedSocket.send(packet)
        #print(packet)
        return parseStatusCode(self.wrappedSocket.recv())
        #return self.wrappedSocket.recv()
    def goToColorFull(self, level, vibrancy, hue, saturation, fadeTime="00:00:05", delayTime="00:00:00"):
        packet = leapjson.goToColorPacket % (self.zoneId, level, vibrancy, hue, saturation, delayTime, fadeTime)
        packet = packet.encode('utf-8')
        self.wrappedSocket.send(packet)
        #print(packet)
        return parseStatusCode(self.wrappedSocket.recv())
        #return self.wrappedSocket.recv()

if __name__ == '__main__':
    print("This is a library, and is NOT meant to run standalone.")
    print("(But you can try some examples to see how it works!)")
