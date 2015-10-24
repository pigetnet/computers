#!/usr/bin/python
import sqlite3
import json
import HTMLParser
from collections import defaultdict


def id2ip(db, id):
    dbActions = db.execute('SELECT ipaddress FROM Config WHERE id='+str(id))
    ips = dbActions.fetchall()
    try:
        ip = ips[0][0]
    except:
        ip = ""
    return str(ip)


def change(id, state):
    print "KANA : ID="+str(id)+" STATE="+str(int(state))
    try:
        db = sqlite3.connect('/user/config/kana/objects/computers.db')
        db.execute('UPDATE Actions SET state='+str(int(state))+' WHERE id='+str(id))
        db.commit()
        db.close()
    except Exception as e:
        print "ERROR: DATABASE"
        print e


def getIP():
    db = sqlite3.connect('/user/config/kana/objects/computers.db')
    dbActions = db.execute('SELECT id,object_key FROM Actions')
    computersActionsTuples = dbActions.fetchall()

    actions = defaultdict(list)
    ips = []

    HTMLParse = HTMLParser.HTMLParser()
    for computerAction in computersActionsTuples:
        actionID = computerAction[0]
        ip = id2ip(db, computerAction[1])
        ips.append(ip)
        actions[ip].append(actionID)
    # Remove duplicate
    ips = list(set(ips))
    db.close()
    return ips, actions


def checkComputers(ipToCheck, actions, state):
    for actionID in actions[ipToCheck]:
        change(actionID, state)
