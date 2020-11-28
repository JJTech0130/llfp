#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
llfp by JJTech0130 - a Lutron LEAP library for Python
https://github.com/LLFP/llfp

'''

import json
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

class area():

    def __init__(self, parent, href):
        self._href = href
        self._parent = parent
        self._leap = self._parent.leap
        summary = self._getsummary()['Body']['Area']
        self._href = summary['href'] # Prefer absolute href as returned by getsummary over any realative one we were given (for eg. /area/3 over /area/rootarea)
        self._name = summary['Name'] # Human readable name
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
        children = []
        packet = {
            "CommuniqueType": "ReadRequest",
            "Header": {
                "Url": str(self._href) + "/childarea/summary"
            }
        }
        childareas = self._leap.send(packet)

        try:
            childlist = childareas['Body']['AreaSummaries']
            for child in childlist:
                if child['IsLeaf'] == 'true':
                    childobj = leafArea(self, child['href'])
                    children.append(childobj)
                else:
                    childobj = area(self, child['href'])
                    children.append(childobj)
        except KeyError:
            # This is not supposed to happen...
            warnings.warn("Branch area has no children...")

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
        try:
            associatedzones = self._getsummary()['Body']['Area']['AssociatedZones']
            for associatedzone in associatedzones:
                zoneobj = zone.create(self, associatedzone['href'])
                children.append(zoneobj)
        except KeyError:
            # We don't seem to have any children...
            pass

        return children

class zone():

    @classmethod
    def create(cls, parent, href):
        ztype = cls.getsummary(parent.leap, href)['Body']['Zone']['ControlType']
        if ztype == 'Switched':
            z = switchedZone(parent, href)
        elif ztype == 'Dimmed':
            z = dimmedZone(parent, href)
        elif ztype == 'SpectrumTune':
            z = spectrumTuningZone(parent, href)
        else:
            warnings.warn("Unsupported Zone Type: " + ztype)
            z = zone(parent, href) # Just create a generic zone
        
        return z
        
    def __init__(self, parent, href):
        self._href = href
        self._parent = parent
        self._leap = self._parent.leap
        summary = self.getsummary(self._leap, self._href)['Body']['Zone']
        self._href = summary['href'] # Prefer absolute href as returned by getsummary over any realative one we were given (for eg. /area/3 over /area/rootarea)
        self._name = summary['Name'] # Human readable name
        self._type = summary['ControlType'] # Type of zone

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

# Zone Subclasses

class switchedZone(zone):

    # Private Functions
    def _getstate(self):
        # Return True or False
        state = self._getstatus()['Body']['ZoneStatus']['SwitchedLevel']
        if state == "On":
            return True
        else:
            return False

    def _setstate(self, state):
        # Accept True or False
        if state == True:
            s = "On"
        else:
            s = "Off"

        packet = {
            "CommuniqueType": "CreateRequest",
            "Header": {
                "Url": self._href + "/commandprocessor",
            },
            "Body": {
                "Command": {
                    "CommandType": "GoToSwitchedLevel",
                    "SwitchedLevelParameters": {
                        "SwitchedLevel": s,
                        "DelayTime":"00:00:01"
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
                        "FadeTime":"00:00:01",
                        "DelayTime":"00:00:01"
                    }
                }
            }
        }
        
        return self._leap.send(packet)

    # Properties
    @property
    def level(self):
        return self._getlevel()

    @level.setter
    def level(self, level):
        self._setlevel(level)


class spectrumTuningZone(zone):
    # TODO: Support spectrum tuning
    pass