import time
import fsm
import numpy as np
import sys


def doWait():
    print("Waiting 1 sec ...")
    time.sleep(1)
    return "wait"


def doInit():
    return "wait"


if __name__ == "__main__":
    f = fsm.fsm()
    f.load_fsm_from_file("fsm_quad_cmd.txt")
    run = True
    while run:
        funct = f.run()
        if f.curState != f.endState:
            newEvent = funct()
            if newEvent is None:
                break
            else:
                f.set_event(newEvent)
        else:
            funct()
            run = False
else:
    pass
    # Init objet quadrotor
