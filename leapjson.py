loginPacket = """{"CommuniqueType": "UpdateRequest","Header": {"Url": "/login"},"Body": {"Login": {"ContextType": "Application","LoginId": "%s","Password": "%s"}}}\r\n"""
goToLevelPacket = """{"CommuniqueType":"CreateRequest","Header":{"Url":"/zone/%d/commandprocessor"},"Body":{"Command":{"CommandType":"GoToDimmedLevel","DimmedLevelParameters":{"Level":%d,"FadeTime":"%s","DelayTime":"%s"}}}}\r\n"""
pingPacket = """{"CommuniqueType":"ReadRequest","Header":{"URL":"/server/status/ping"}}\r\n"""
readDevicePacket = """{"CommuniqueType":"ReadRequest","Header":{"URL":"/device"}}\r\n"""
