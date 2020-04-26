# NOTE: You will need to put llfp.py and leapjson.py in the
#  same folder as basic.py in order for this to work!!!
import llfp
# Setup connection and login
bridge1 = llfp.bridge("192.168.0.5")
print(bridge1.login("jjtech", "jjtech0130")) #Replace with your username/password.
# Control zone
zone1 = llfp.zone(6164, bridge1) #Replace 690 with the number of the zone you want to control.
#print(zone1.goToColorFull(100,50,237,100)) #Replace 0 with a number 0-100
print(zone1.goToColor(100,309))
