#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
llfp by JJTech0130 - a Lutron LEAP For Python library
https://github.com/LLFP/llfp

'''

import json
import socket, ssl
import colorsys
import warnings

DEBUG = False

class leap:
    '''
    low-level LEAP commmands
    '''
    def __init__(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        self.__sock = ssl.wrap_socket(sock)
        self.__sock.connect((host,port))

    def send(self, packet):
        packet = json.dumps(packet) # Turn it into JSON
        packet += '\r\n' # Add a newline
        packet = packet.encode('utf-8') # Encode it in UTF-8
        self.__sock.send(packet) # Send the packet
        return json.loads(self.__sock.recv().decode('utf-8')) # Decode the result

    def read(self, url):
        packet = {
            "CommuniqueType": "ReadRequest",
            "Header": {
                "Url": str(url)
            }
        }

        return self.send(packet)

    def run(self, url, command):
        packet = {
            "CommuniqueType": "CreateRequest",
            "Header": {
                "Url": str(url)
            },
            "Body": {
                "Command": command
            }
        }

        return self.send(packet)

    # TODO: Run periodically to keep the connection allive
    def ping(self):
        return self.read("/server/status/ping")

    # Compat.
    @property
    def sock(self):
        return self.__sock

class bridge:
    '''
    Control the bridge/processor
    '''
    def __init__(self, host, port=8081):
        self.__leap = leap(host,port)


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

        return self.__leap.send(packet)

    @property
    def leap(self):
        return self.__leap

    @property
    def root(self):
        return area(self, "/area/rootarea")

class area():
    '''
    Area object
    '''
    def __init__(self, parent, href):
        self.__href = href
        self.__parent = parent
        self.__leap = self.__parent.leap
        summary = self.__getsummary()['Body']['Area']
        self.__href = summary['href'] # Prefer absolute href as returned by getsummary over any realative one we were given (for eg. /area/3 over /area/rootarea)
        self.__name = summary['Name'] # Human readable name
        self.__children = self.__getchildren() # Save children as private variable so we don't end up with repeat objects

    # Private functions
    def __getsummary(self):
        packet = {
            "CommuniqueType": "ReadRequest",
            "Header": {
                "Url": str(self.__href)
            }
        }

        return self.__leap.send(packet)

    def __getchildareas(self):
        packet = {
            "CommuniqueType": "ReadRequest",
            "Header": {
                "Url": str(self.__href) + "/childarea/summary"
            }
        }

        return self.__leap.send(packet)


    def __getchildren(self):
        children = []
        # Try to get child areas
        try:
            childlist = self.__getchildareas()['Body']['AreaSummaries']
            for child in childlist:
                childobj = area(self, child['href'])
                children.append(childobj)
        except KeyError:
            # We are a leaf, so see if we have any zones
            self.__leaf = True # Probably a better way, but this is how we tell for now.
            try:
                associatedzones = self.__getsummary()['Body']['Area']['AssociatedZones']
                for associatedzone in associatedzones:
                    zoneobj = zone(self, associatedzone['href'])
                    children.append(zoneobj)
            except KeyError:
                # We don't seem to have any children...
                pass

        return children

    # Properties
    @property
    def children(self):
        return self.__children.copy() # Lists are not automatically passed as copies

    @property
    def name(self):
        return self.__name

    @property
    def href(self):
        return self.__href

    @property
    def leaf(self):
        return self.__leaf

    @property
    def parent(self):
        return self.__parent

    @property
    def leap(self):
        return self.__leap

class zone():
    '''
    Controlling zones
    '''
    def __init__(self, parent, href):
        self.__href = href
        self.__parent = parent
        self.__leap = self.__parent.leap
        summary = self.__getsummary()['Body']['Zone']
        self.__href = summary['href'] # Prefer absolute href as returned by getsummary over any realative one we were given (for eg. /area/3 over /area/rootarea)
        self.__name = summary['Name'] # Human readable name
        self.__type = summary['ControlType'] # Type of zone
        self.__tune = self.__gettune()

    # Private functions
    def __getsummary(self):
        packet = {
            "CommuniqueType": "ReadRequest",
            "Header": {
                "Url": str(self.__href)
            }
        }

        return self.__leap.send(packet)

    def __getstatus(self):
        packet = {
            "CommuniqueType": "ReadRequest",
            "Header": {
                "Url": str(self.__href) + "/status"
            }
        }

        return self.__leap.send(packet)

    def __gettune(self):
        status = self.__getstatus()['Body']['ZoneStatus']
        
        # Refresh tune using .get to avoid KeyErrors
        tune = {
            'Level': status.get('Level'),
            'Vibrancy': status.get('Vibrancy'),
            'ColorTuningStatus': {
                'HSVTuningLevel': status.get('ColorTuningStatus')['HSVTuningLevel'] if status.get('ColorTuningStatus') != None else None
            }
            #'hue': status.get('ColorTuningStatus')['HSVTuningLevel']['Hue'],
            #'saturation': status.get('ColorTuningStatus')['HSVTuningLevel']['Saturation']
        }

        return tune

    def __settune(self):
        packet = {
                "CommuniqueType": "CreateRequest",
                "Header": {
                    "Url": self.__href + "/commandprocessor",
                },
                "Body": {
                    "Command": {
                        "CommandType": "GoToSpectrumTuningLevel",
                        "SpectrumTuningLevelParameters": {
                            "FadeTime":"00:00:00",
                            "DelayTime":"00:00:00"
                        }
                    }
                }
            }
        
        for p in self.__tune:
            packet['Body']['Command']['SpectrumTuningLevelParameters'][p] = self.__tune[p]

        #print(packet)

        return self.__leap.send(packet)

    @property
    def level(self):
        self.__tune = self.__gettune()
        return self.__tune['Level']

    @level.setter
    def level(self, value):
        self.__tune = self.__gettune()
        self.__tune['Level'] = value

        # If level is 0, delete all other keys before sending
        if value == 0:
            for p in self.__tune.copy():
                if p != 'Level':
                    del self.__tune[p]
        
        self.__settune()
        self.__tune = self.__gettune() # Reset it

    @property
    def delay(self):
        pass

    @delay.setter
    def delay(self, value):
        pass


    @property
    def hue(self):
        pass

    @hue.setter
    def hue(self, value):
        pass


    @property
    def vibrancy(self):
        pass

    @vibrancy.setter
    def vibrancy(self, value):
        pass


    @property
    def saturation(self):
        pass

    @saturation.setter
    def saturation(self, value):
        pass


    @property
    def fade(self):
        pass

    @fade.setter
    def fade(self, value):
        pass

    # Properties
    @property
    def name(self):
        return self.__name

    @property
    def href(self):
        return self.__href

    @property
    def parent(self):
        return self.__parent

    @property
    def leap(self):
        return self.__leap

    @property
    def type(self):
        return self.__type

# Zone Subclasses
class switchedZone(zone):
    def __init__(self, parent, href):
        super().__init__(parent, href)
        if self.__type != 'Switched':
            warnings.warn("Zone Type Mismatch!")

class dimmedZone(zone):
    pass

class spectrumTuningZone(zone):
    pass