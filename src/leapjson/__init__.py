# LEAP JSON File
# Declares the different JSON structures used for messages.
# Used by LLFP (Lutron LEAP For Python)
loginPacket = """{"CommuniqueType": "UpdateRequest","Header": {"Url": "/login"},"Body": {"Login": {"ContextType": "Application","LoginId": "%s","Password": "%s"}}}\r\n"""
goToLevelPacket = """{"CommuniqueType":"CreateRequest","Header":{"Url":"/zone/%d/commandprocessor"},"Body":{"Command":{"CommandType":"GoToDimmedLevel","DimmedLevelParameters":{"Level":%d,"FadeTime":"%s","DelayTime":"%s"}}}}\r\n"""
pingPacket = """{"CommuniqueType":"ReadRequest","Header":{"Url":"/server/status/ping"}}\r\n"""
goToColorPacket = """{"CommuniqueType":"CreateRequest","Header":{"Url":"/zone/%d/commandprocessor"},"Body":{"Command":{"CommandType":"GoToSpectrumTuningLevel","SpectrumTuningLevelParameters":{"Level":%d,"Vibrancy":%d,"ColorTuningStatus":{"HSVTuningLevel":{"Hue":%d,"Saturation":%d}},"DelayTime":"%s","FadeTime":"%s"}}}}\r\n"""
readDevicePacket = """{"CommuniqueType":"ReadRequest","Header":{"Url":"/device/%d"}}\r\n"""
zoneStatusPacket = """{"CommuniqueType":"ReadRequest","Header":{"Url":"/zone/%d/status"}}\r\n"""
goToWhiteLevelPacket = """{"CommuniqueType":"CreateRequest","Header":{"Url":"/zone/%d/commandprocessor"},"Body":{"Command":{"CommandType":"GoToSpectrumTuningLevel","SpectrumTuningLevelParameters":{"Level":%d,"Vibrancy":%d,"ColorTuningStatus":{"WhiteTuningLevel":{"Kelvin":%d}},"DelayTime":"%s","FadeTime":"%s"}}}}\r\n"""
