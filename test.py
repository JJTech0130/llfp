import llfp, time
b = llfp.bridge("192.168.4.37")
b.login("jjtech", "jjtech0130")

def find_zone(room, name):
    for area in b.root.children:
        for subarea in area.children:
            for zone in subarea.children:
                if zone.name == name and zone.parent.name == room:
                    return zone
# Liam: /zone/8380
# Jay: /zone/7690
# Micah: /zone/7708
print("Finding zones by name... this is *really* inefficient...")
light1 = find_zone("Micah's Room", "Lights")
light2 = find_zone("Liams Room", "Lights")
light3 = find_zone("Jays Room", "Lights")
print("Found all the zones!")
#light1 = llfp.switchedZone(b.root, "/zone/7708")
#light2 = llfp.switchedZone(b.root, "/zone/8380")
#light3 = llfp.switchedZone(b.root, "/zone/7690")
light1.delay = 0
light2.delay = 0
light3.delay = 0
#jay.state = not jay.state
while True:
    # wait for the user to press enter
    input("Press Enter to toggle the lights...")
    #print(light3.state)
    light1.state = not light1.state
    light2.state = not light2.state
    light3.state = not light3.state
#for area in a.children:
    #print(area.name)
    #print(area.href)
#    for area2 in area.children:
#        #print(area2.name)
#        for area3 in area2.children:
#            print(area2.name + " " + area3.name + " is at " + area3.href + " and is a " + area3.type)
#            if area2.name == 'Jays Room' and area3.name == 'Lights':
#                area3.delay = 0
#                area3.state = not area3.state
        #print(area2.children)
#test = llfp.switchedZone(jaysroomarea, jaysroom.href)
#print(test.state)
#test.state = not test.state