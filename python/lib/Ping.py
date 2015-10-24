import os
from lib import State


def ping(ip):
    ret = os.system("ping -c 1 -w 1 "+ip+">/dev/null")
    if ret == 0:
        print "Ping:"+str(ip)+" is up"
        return True
    else:
        print "Ping:"+str(ip)+" is down"
        return False


def all(ips, actions):
    states = []
    for ip in ips:
        print ip
        initial_state = ping(str(ip))
        state = {}
        state["ip"] = ip
        state["state"] = initial_state
        state["flapping"] = 0
        states.append(state)
        State.checkComputers(ip, actions, initial_state)

    # print states
    return states


def checkState(state):
    new_state = ping(state["ip"])
    old_state = state["state"]
    if(new_state != old_state):
        state["flapping"] += 1
        print state["ip"] + " seems to have changed for " + str(state["flapping"])
        if(state["flapping"] >= 3):
            print state["ip"] + "have changed"
            state["state"] = new_state
            state["flapping"] = 0
            result = True
        else:
            result = False
    else:
        state["flapping"] = 0
        result = False
    return state, result
