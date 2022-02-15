import llfp, time
b = llfp.bridge("192.168.4.37")
b.login("jjtech", "jjtech0130")
a = b.root
for area in a.children:
    #print(area.name)
    #print(area.href)
    for area2 in area.children:
        #print(area2.name)
        for area3 in area2.children:
            print(area2.name + " " + area3.name + " is at " + area3.href + " and is a " + area3.type)
        #print(area2.children)
#test = llfp.switchedZone(jaysroomarea, jaysroom.href)
#print(test.state)
#test.state = not test.state