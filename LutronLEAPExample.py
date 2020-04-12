import socket
import ssl

# Define variables
HOST, PORT = '192.168.0.5', 8085 #Replace with the IP of the device
loginPacket = """{"CommuniqueType": "UpdateRequest","Header": {"Url": "/login"},"Body": {"Login": {"ContextType": "Application","LoginId": "%s","Password": "%s"}}}\r\n"""
goToLevelPacket = """{"CommuniqueType":"CreateRequest","Header":{"Url":"/zone/%d/commandprocessor"},"Body":{"Command":{"CommandType":"GoToDimmedLevel","DimmedLevelParameters":{"Level":%d,"FadeTime":"%s","DelayTime":"%s"}}}}\r\n"""

# Establish connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)
wrappedSocket = ssl.wrap_socket(sock)
wrappedSocket.connect((HOST, PORT))

# Define commands
def login(loginId, password):
    wrappedSocket.send(loginPacket % (loginId, password))
    #print wrappedSocket.recv()

def goToLevel(zone, level, fadeTime="00:00:05", delayTime="00:00:00"):
    wrappedSocket.send(goToLevelPacket % (zone, level, fadeTime, delayTime))
    #print wrappedSocket.recv()

# Run commands
login("username","password") #REPLACE WITH YOUR USERNAME/PASSWORD
goToLevel(690, 100) #690 is an example, replace with your zone number
