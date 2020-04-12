import leapjson
import socket
import ssl

class leap:
    "Main LEAP class"
    def __init__(self, host, port=8085):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        self.wrappedSocket = ssl.wrap_socket(sock)
        self.wrappedSocket.connect((host, port))
    def login(self, loginId, password):
        self.wrappedSocket.send(leapjson.loginPacket % (loginId, password))
        #print(self.wrappedSocket.recv())
    def goToLevel(self, zone, level, fadeTime="00:00:05", delayTime="00:00:00"):
        self.wrappedSocket.send(leapjson.goToLevelPacket % (zone, level, fadeTime, delayTime))
        print(self.wrappedSocket.recv())
