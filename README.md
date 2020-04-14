# LLFP - Lutron LEAP For Python
This is a python library for using Lutron's LEAP control protocol.

## Examples
### Basic usage
First, you need to setup a connection with the ```bridge``` object.
For example:
```python
import llfp
# Setup connection and login
bridge1 = llfp.bridge("192.168.0.5")
print(bridge1.login("yourUsername", "yourPassword")) #Replace with your username/password.
# Control zone
zone1 = llfp.zone(690, bridge1) #Replace 690 with the number of the zone you want to control.
print(zone1.goToLevel(0)) #Replace 0 with a number 0-100
```
## TODO

- [x] Get basic things (login, set level, ping, etc.)
- [x] Use seperate classes
- [ ] Make sure that things work correctly when they finally get implimented
- [ ] Add proper documentation
