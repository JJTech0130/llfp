# LEAP JSON File
# Declares the different JSON structures used for messages.
# Used by LLFP (Lutron LEAP For Python)
loginPacket = """{"CommuniqueType": "UpdateRequest","Header": {"Url": "/login"},"Body": {"Login": {"ContextType": "Application","LoginId": "%s","Password": "%s"}}}\r\n"""
goToLevelPacket = """{"CommuniqueType":"CreateRequest","Header":{"Url":"/zone/%d/commandprocessor"},"Body":{"Command":{"CommandType":"GoToDimmedLevel","DimmedLevelParameters":{"Level":%d,"FadeTime":"%s","DelayTime":"%s"}}}}\r\n"""
pingPacket = b"""{"CommuniqueType":"ReadRequest","Header":{"Url":"/server/status/ping"}}\r\n"""
readDevicePacket = b"""{"CommuniqueType":"ReadRequest","Header":{"Url":"/device%b"}}\r\n"""
getZonesPacket = b"""{"CommuniqueType":"ReadRequest","Header":{"Url":"/zone"}}\r\n"""
