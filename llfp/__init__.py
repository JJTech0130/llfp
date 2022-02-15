#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
llfp by JJTech0130 - a Lutron LEAP library for Python
https://github.com/LLFP/llfp

'''

import json
import time
import socket, ssl
import colorsys
import warnings


class leap:
    '''
    low-level LEAP commmands
    '''
    def __init__(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        self._sock = ssl.wrap_socket(sock)
        self._sock.connect((host,port))

    def send(self, packet):
        packet = json.dumps(packet) # Turn it into JSON
        packet += '\r\n' # Add a newline
        packet = packet.encode('utf-8') # Encode it in UTF-8
        self._sock.send(packet) # Send the packet
        return json.loads(self._sock.recv().decode('utf-8')) # Decode the result

    # TODO: Run periodically to keep the connection allive
    def ping(self):
        packet = {
            "CommuniqueType": "ReadRequest",
            "Header": {
                "Url": "/server/status/ping"
            }
        }

        return self.send(packet)

    # Compat.
    @property
    def sock(self):
        return self._sock

class bridge:
    '''
    Control the bridge/processor
    '''
    def __init__(self, host, port=8081):
        self._leap = leap(host,port)


    def login(self, id, password):
        packet = {
            "CommuniqueType": "UpdateRequest",
            "Header": {
                "Url": "/login"
            },
            "Body": {
                "Login": {
                    "ContextType": "Application",
                    "LoginID": id,
                    "Password": password
                }
            }
        }

        return self._leap.send(packet)

    @property
    def leap(self):
        return self._leap

    @property
    def root(self):
        return area(self, "/area/rootarea")

# Helper function to format seconds as HH:MM:SS
def format_seconds(sec):
    return time.strftime('%H:%M:%S', time.gmtime(sec))

def parse_seconds(time_str):
    return time.strptime(time_str, "%H:%M:%S")

class area():

    def __init__(self, parent, href):
        self._href = href
        self._parent = parent
        self._leap = self._parent.leap
        self._summary = self._getsummary()['Body']['Area']
        self._href = self._summary['href'] # Prefer absolute href as returned by getsummary over any realative one we were given (for eg. /area/3 over /area/rootarea)
        self._name = self._summary['Name'] # Human readable name
        self._children = self._getchildren() # Save children as private variable so we don't end up with repeat objects

    # Private functions
    def _getsummary(self):
        packet = {
            "CommuniqueType": "ReadRequest",
            "Header": {
                "Url": str(self._href)
            }
        }

        return self._leap.send(packet)

    def _getchildren(self):
        packet = {
            "CommuniqueType": "ReadRequest",
            "Header": {
                "Url": str(self._href) + "/childarea/summary" # can't use getsummary as it doesn't return child areas
            }
        }

        response = self._leap.send(packet)

        children = []

        if 'AreaSummaries' in response['Body']:
            for child in response['Body']['AreaSummaries']:
                if child['IsLeaf']:
                    children.append(leafArea(self, child['href']))
                else:
                    children.append(area(self, child['href']))
        else:
            warnings.warn("No children found for " + self.name)

        return children

    # Properties
    @property
    def children(self):
        return self._getchildren().copy() # Lists are not automatically passed as copies

    @property
    def name(self):
        return self._name

    @property
    def href(self):
        return self._href

    @property
    def parent(self):
        return self._parent

    @property
    def leap(self):
        return self._leap

class leafArea(area):

     def _getchildren(self):
        children = []
        # We are a leaf, so see if we have any zones
        if 'AssociatedZones' in self._summary:
            for zone_ in self._summary['AssociatedZones']:
                children.append(zone.create(self, zone_['href']))

        return children

class zone():

    @classmethod
    def create(cls, parent, href):
        ztype = cls.getsummary(parent.leap, href)['Body']['Zone']['ControlType']
        match ztype:
            case 'Switched': return switchedZone(parent, href)
            case 'Dimmed': return dimmedZone(parent, href)
            case 'SpectrumTune': return spectrumTuningZone(parent, href)
            case _:
                warnings.warn("Unknown zone type: " + ztype)
                return zone(parent, href)
        
    def __init__(self, parent, href):
        self._href = href
        self._parent = parent
        self._leap = self._parent.leap
        summary = self.getsummary(self._leap, self._href)['Body']['Zone']
        self._href = summary['href'] # Prefer absolute href as returned by getsummary over any realative one we were given (for eg. /area/3 over /area/rootarea)
        self._name = summary['Name'] # Human readable name
        self._type = summary['ControlType'] # Type of zone
        self.delay = 0 # Default to no delay

    @staticmethod
    def getsummary(leap, href):
        packet = {
            "CommuniqueType": "ReadRequest",
            "Header": {
                "Url": str(href)
            }
        }

        return leap.send(packet)

    def _getstatus(self):
        packet = {
            "CommuniqueType": "ReadRequest",
            "Header": {
                "Url": str(self._href) + "/status"
            }
        }

        return self._leap.send(packet)

    # Properties
    @property
    def name(self):
        return self._name

    @property
    def href(self):
        return self._href

    @property
    def parent(self):
        return self._parent

    @property
    def leap(self):
        return self._leap

    @property
    def type(self):
        return self._type

    @property
    def delay(self):
        return parse_seconds(self._delay)

    @delay.setter
    def delay(self, value):
        self._delay = format_seconds(value)

# Zone Subclasses

class switchedZone(zone):
    
    # Private Functions
    def _getstate(self):
        # Return True or False
        state = self._getstatus()['Body']['ZoneStatus']['SwitchedLevel']
        return state == 'On'

    def _setstate(self, state):
        packet = {
            "CommuniqueType": "CreateRequest",
            "Header": {
                "Url": self._href + "/commandprocessor",
            },
            "Body": {
                "Command": {
                    "CommandType": "GoToSwitchedLevel",
                    "SwitchedLevelParameters": {
                        "SwitchedLevel": "On" if state else "Off",
                        "DelayTime": self._delay
                    }
                }
            }
        }
        
        return self._leap.send(packet)

    # Properties
    @property
    def state(self):
        return self._getstate()

    @state.setter
    def state(self, state):
        self._setstate(state)


class dimmedZone(zone):

    def __init__(self, parent, href):
        self._fade = 1
        super().__init__(parent, href)

    # Private Functions
    def _getlevel(self):
        # Return percentage
        state = self._getstatus()['Body']['ZoneStatus']['Level']
        return state

    def _setlevel(self, level):
        # Accept percentages
        if level > 100 or level < 0:
            raise Exception("Level must be a percentage between 0 and 100")

        packet = {
            "CommuniqueType": "CreateRequest",
            "Header": {
                "Url": self._href + "/commandprocessor",
            },
            "Body": {
                "Command": {
                    "CommandType": "GoToDimmedLevel",
                    "DimmedLevelParameters": {
                        "Level": level,
                        "FadeTime": self._fade,
                        "DelayTime": self._delay
                    }
                }
            }
        }
        
        return self._leap.send(packet)

    # Properties
    @property
    def fade(self):
        return parse_seconds(self._fade)

    @fade.setter
    def fade(self, value):
        self._fade = format_seconds(value)

    @property
    def level(self):
        return self._getlevel()

    @level.setter
    def level(self, level):
        self._setlevel(level)


class spectrumTuningZone(zone):
    # TODO: Support spectrum tuning
    pass