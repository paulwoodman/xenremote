#!/usr/bin/env python

# XenServer XAPI CL interface
#
# (C) 2014 Wilhelm Babernits <wbabernits@onenext.de>

import XenAPI
import XenRemote
from configobj import ConfigObj


name = 'xenremote'
version = '0.0.1'
level = 'alpha'

conf = ConfigObj("xenremote.conf")

session = XenAPI.Session(conf["url"])
session.xenapi.login_with_password(conf["user"], conf["pass"])
remote = XenRemote.Vmcontrol(session)

while(True):
    # interactive console
    action = raw_input('xenremote >> ')

    # start a virtual machine
    if(action=='start'):
        remote.get_halted_vm_list()
        remote.get_suspended_vm_list()
        remote.get_paused_vm_list()
        uuid = raw_input('uuid >> ')
        if(remote.start_vm_by_uuid(uuid)):
            print('vm started')
        else:
            print('vm cannot be started')

    # shutdown a virtual machine
    elif(action=='shutdown'):
        remote.get_running_vm_list()
        remote.get_suspended_vm_list()
        remote.get_paused_vm_list()
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

    # pause a virtual machine
    elif(action=='pause'):
        remote.get_running_vm_list()
        uuid = raw_input('uuid >> ')
        if(remote.pause_vm_by_uuid(uuid)):
            print('vm paused')
        else:
            print('vm cannot be paused')

    # show the status of all virtual machines
    elif(action=='status'):
        remote.get_vm_status_list()

    # show help options
    elif(action=='help'):
        print("XenRemote (C) 2014 W. Babernits <wbabernits@onenext.de>\n")
        print("available commands:\nstart, shutdown, suspend, status, help, version, exit\n")

    # print xenremote version
    elif(action=='version'):
        print(name + "/" + version + "-" + level)

    # exit program
    elif(action=='exit'):
        print('program terminated by user')
        exit()

    # unknown command
    else:
        print('unknown command: type help for a list of available commands')
