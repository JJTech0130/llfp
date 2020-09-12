import llfp, time
b = llfp.bridge("192.168.0.5")
b.login("jjtech", "jjtech0130")
a = b.root

while 1:
    for child in a.children:
        if child.name == 'Main Floor':
            for gchild in child.children:
                if gchild.name == 'Living Room':
                    for zone in gchild.children:
                        if zone.level == 0:
                            zone.level = 100
                        else:
                            zone.level = 0
    time.sleep(1.5)
