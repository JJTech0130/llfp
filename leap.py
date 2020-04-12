import leapjson
import socket
import ssl

class leap:
    "Main LEAP class"
    def __init__(self, host, port=8085):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        wrappedSocket = ssl.wrap_socket(sock)
        wrappedSocket.connect((host, port))
    def login(self, loginId, password):
        wrappedSocket.send(leapjson.loginPacket % (loginId, password))
        print(wrappedSocket.recv())
    def goToLevel(self, zone, level, fadeTime="00:00:05", delayTime="00:00:00"):
        wrappedSocket.send(goToLevelPacket % (zone, level, fadeTime, delayTime))
        print(wrappedSocket.recv())
