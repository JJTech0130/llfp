# NOTE: You will need to put llfp.py and leapjson.py in the
#  same folder as basic.py in order for this to work!!!
import llfp
# Setup connection and login
bridge1 = llfp.bridge("192.168.0.5")
print(bridge1.login("yourUsername", "yourPassword")) #Replace with your username/password.
# Control zone
zone1 = llfp.zone(690, bridge1) #Replace 690 with the number of the zone you want to control.
print(zone1.goToLevel(0)) #Replace 0 with a number 0-100
