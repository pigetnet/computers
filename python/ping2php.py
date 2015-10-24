#!/usr/bin/python
from lib import Socket
from lib import PhpRequest
from lib import Ping
from lib import State
import sys
import time
import os
import sqlite3

"""Main"""

"""Variables"""
global path
sleep_between_ping = 3
last_data = ""
lock = False
data = False
path = "/do/kana/www/"

"""
Get ip from database on Kana
@todo make it usable without kana
"""

# Get port
with open('/do/computers/python/port', 'r') as port_file:
    content = port_file.read()
    socket_port = int(content.strip())
Socket.Start(socket_port)
print "Socket Started"

ips, actions = State.getIP()
ip_states = Ping.all(ips, actions)

try:
    while True:
        time.sleep(sleep_between_ping)

        for i, ip_state in enumerate(ip_states):
            state, result = Ping.checkState(ip_state)
            ip_states[i] = state
            if(result):
                data = state["ip"]
                if state["state"]:
                    State.checkComputers(ip, actions, 1)
                    state = "on"
                else:
                    State.checkComputers(ip, actions, 1)
                    state = "off"
                print "SENDING-----"
                print "IP:" + data + " " + state
                PhpRequest.send(path, "/computers/"+data, state)
                Socket.Send(data+";"+state)
                print "SENDING-----"

except KeyboardInterrupt:
    Socket.Close()
    os._exit(13)
