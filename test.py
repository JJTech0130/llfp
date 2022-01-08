import llfp, time
b = llfp.bridge("192.168.0.5")
b.login("jjtech", "jjtech0130")
a = b.root
upstairs = a.children[1]
jaysroomarea = upstairs.children[2]
jaysroom = jaysroomarea.children[0]
print(type(jaysroom))
#test = llfp.switchedZone(jaysroomarea, jaysroom.href)
#print(test.state)
#test.state = not test.state