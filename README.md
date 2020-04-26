# llfp - Lutron LEAP For Python

This is a python library for using Lutron's LEAP control protocol.

## Examples
### Installing
First, get the .whl file from [here](https://github.com/JJTech0130/llfp/releases)

Then, run the command
`pip3 install llfp-*.*.*-py3-none-any.whl`
(Replace the '\*'s with the version of llfp you downloaded)

> **Note:** Currently, this is only available for python3. In the future, python 2 support *may* be added.
### Basic usage

First, you need to setup a connection with the ```bridge``` object.
For example:

```python
import llfp
# Setup connection and login
bridge1 = llfp.bridge("192.168.0.5") #Replace with the IP address of your bridge
print(bridge1.login("yourUsername", "yourPassword")) #Replace with your username/password.
```

Next, you need to define a zone object.

```python
# Control zone
zone1 = llfp.zone(690, bridge1) #Replace 690 with the number of the zone you want to control.
```

> **Note**: As of right now, the current LEAP implementation does NOT support reading back zone numbers, so you will have to find this out elsewhere.

Then, you can do something.

```python
print(zone1.goToLevel(0)) #Replace 0 with a number 0-100
```

> For more examples and things to try, you can check the **examples** folder

## TODO

- [x] Get basic things (login, set level, ping, etc.)
- [x] Use seperate classes
- [x] Make sure that things work correctly when they finally get implemented
- [x] Add more features (color, etc.)
- [ ] Document all the features
