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
        packet = leapjson.loginPacket % (loginId, password)
        packet = packet.encode('utf-8')
        self.wrappedSocket.send(packet)
        print(self.wrappedSocket.recv())
    def goToLevel(self, zone, level, fadeTime="00:00:05", delayTime="00:00:00"):
        """This tells a zone to go to a specific level."""
        packet = leapjson.goToLevelPacket % (zone, level, fadeTime, delayTime)
        packet = packet.encode('utf-8')
        self.wrappedSocket.send(packet)
        print(self.wrappedSocket.recv())
    def ping(self):
        """This is the ping command. Acts like it sounds."""
        self.wrappedSocket.send(leapjson.pingPacket.encode('utf-8'))
        print(self.wrappedSocket.recv())
