import leapjson
import socket
import ssl

class leap:
    """
    Main LEAP class.
    Example:
    import llfp
    myleap = llfp.leap("192.168,0,5") #Replace "192.168.0.5" with devices IP
    myleap.login("loginId","password")
    myleap.goToLevel(2,100) #2 is the zone id and 100 is the level to go to
    """
    def __init__(self, host, port=8085):
        """This is called when you initialize the class."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        self.wrappedSocket = ssl.wrap_socket(sock)
        self.wrappedSocket.connect((host, port))
    def login(self, loginId, password):
        """This sends the login packet to the device."""
        self.wrappedSocket.send(leapjson.loginPacket % (loginId, password))
        print(self.wrappedSocket.recv())
    def goToLevel(self, zone, level, fadeTime="00:00:05", delayTime="00:00:00"):
        """This tells a zone to go to a specific level."""
        self.wrappedSocket.send(leapjson.goToLevelPacket % (zone, level, fadeTime, delayTime))
        print(self.wrappedSocket.recv())
    def ping(self):
        """This is the ping command. Acts like it sounds."""
        self.wrappedSocket.send(leapjson.pingPacket)
        print(self.wrappedSocket.recv())
    def readDevice(self,device=""):
        """
        This is suppossed to read a list of devices, or,
        if you specify a device ID it should return info about
        that device. It has not been implimented on the Lutron side yet.
        """
        self.wrappedSocket.send(leapjson.readDevicePacket % device)
        print(self.wrappedSocket.recv())
