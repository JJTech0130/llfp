# LEAP JSON File
# Declares the different JSON structures used for messages.
# Used by LLFP (Lutron LEAP For Python)
loginPacket = b"""{"CommuniqueType": "UpdateRequest","Header": {"Url": "/login"},"Body": {"Login": {"ContextType": "Application","LoginId": "%b","Password": "%b"}}}\r\n"""
goToLevelPacket = b"""{"CommuniqueType":"CreateRequest","Header":{"Url":"/zone/%d/commandprocessor"},"Body":{"Command":{"CommandType":"GoToDimmedLevel","DimmedLevelParameters":{"Level":%d,"FadeTime":"%s","DelayTime":"%s"}}}}\r\n"""
pingPacket = b"""{"CommuniqueType":"ReadRequest","Header":{"Url":"/server/status/ping"}}\r\n"""
readDevicePacket = b"""{"CommuniqueType":"ReadRequest","Header":{"Url":"/device%s"}}\r\n"""
getZonesPacket = b"""{"CommuniqueType":"ReadRequest","Header":{"Url":"/zone"}}\r\n"""
