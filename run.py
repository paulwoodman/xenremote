#!/usr/bin/env python

# XenServer XAPI CL interface
#
# (C) 2014 Wilhelm Babernits <wbabernits@onenext.de>

import XenAPI
import XenRemote
from configobj import ConfigObj


# Lese Konfiguration
conf = ConfigObj("xenremote.conf")

# Verbindung zum XenServer Host herstellen und Session initialisieren
session = XenAPI.Session(conf["url"])
session.xenapi.login_with_password(conf["user"], conf["pass"])

# Initialisieren der XenRemote Klasse
remote = XenRemote.Vmcontrol(session)

while(True):
    # interactive console
    action = raw_input('xenremote >> ')

    # start a virtual machine
    if(action=='start'):
        remote.get_halted_vm_list()
        remote.get_suspended_vm_list()
        uuid = raw_input('uuid >> ')
        if(remote.start_vm_by_uuid(uuid)):
            print('vm started')
        else:
            print('vm cannot be started')

    # shutdown a virtual machine
    elif(action=='shutdown'):
        remote.get_running_vm_list()
        remote.get_suspended_vm_list()
        uuid = raw_input('uuid >> ')
        if(remote.shutdown_vm_by_uuid(uuid)):
            print('vm stopped')
        else:
            print('vm cannot be stopped')

    # suspend a virtual machine
    elif(action=='suspend'):
        remote.get_running_vm_list()
        uuid = raw_input('uuid >> ')
        if(remote.suspend_vm_by_uuid(uuid)):
            print('vm suspended')
        else:
            print('vm cannot be suspended')

    # show all virtual machines
    elif(action=='status'):
        remote.get_vm_status_list()

    # show help options
    elif(action=='help'):
        print("available commands:\nstart, shutdown, suspend, status, help, exit\n")

    # exit the program
    elif(action=='exit'):
        print('program terminated by user')
        exit()
