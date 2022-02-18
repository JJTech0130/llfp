import logging

import llfp, time

from rich.traceback import install

install(show_locals=True)

from rich import print

b = llfp.Bridge("192.168.4.37")
b.login("jjtech", "jjtech0130")

root = b.root()  # This function will re-index the entire tree, don't call it multiple times


def child(area, name):
    for c in area.children:
        if c.name == name:
            return c


def fmt(zone):
    if isinstance(zone, llfp.LeafArea):
        return "[yellow]" + zone.name + "[/yellow]"
    elif isinstance(zone, llfp.Area):
        return "[blue]" + zone.name + "[/blue]"
    elif isinstance(zone, llfp.DimmedZone):
        return "[cyan]" + zone.name + "[/cyan]"
    else:
        return zone.name


def prompt(loc):
    return "[green]LEAP[/green] " + fmt(loc) + ">> "


loc = root
# loc = child(child(root, "Main Floor"), "Kitchen")
try:
    while True:  # FIXME: Loop blocks, no ping/heartbeat
        print(prompt(loc), end="")
        cmd = input().split(maxsplit=1)
        # print(cmd)
        if cmd:
            if cmd[0] == 'ls' or cmd[0] == 'sl':
                for c in loc.children:
                    print(fmt(c))

            elif cmd[0] == 'cd':
                if cmd[1] == '..':
                    loc = loc.parent
                else:
                    c = cmd[1].split("/")
                    o = loc
                    for i in c:
                        oz = child(o, i)
                        if not oz:
                            print("No such area or zone")
                        else:
                            o = oz
                    if isinstance(o, llfp.Zone):
                        print("Not an area")
                        loc = o.parent
                    else:
                        loc = o

            elif cmd[0] == 'level' or cmd[0] == 'lvl':
                c = cmd[1].split(maxsplit=1)
                # print(c)
                l = child(loc, c[1])
                # print(l)
                if isinstance(l, llfp.DimmedZone):
                    l.level = int(c[0])
                else:
                    print("Invalid zone")

            elif cmd[0] == 'state' or cmd[0] == 'st':
                c = cmd[1].split(maxsplit=1)
                # print(c)
                l = child(loc, c[1])
                # print(l)
                if isinstance(l, llfp.SwitchedZone):
                    if c[0] == 'on':
                        l.state = True
                    else:
                        l.state = False
                else:
                    print("Invalid zone")

            elif cmd[0] == 'dbg':
                llfp.log.setLevel(logging.DEBUG)

            elif cmd[0] == 'exit':
                break
except KeyboardInterrupt:
    pass

# FIXME: Need to close socket?
