#!/usr/bin/env python

# XenServer XAPI CL interface
#
# (C) 2014 Wilhelm Babernits <wbabernits@onenext.de>

import sys
import XenAPI
import XenRemote
from configobj import ConfigObj


name = 'XenRemote'
version = '0.0.2'
level = 'alpha'

conf = ConfigObj("xenremote.conf")

session = XenAPI.Session(conf["url"])

try:
    session.xenapi.login_with_password(conf["user"], conf["pass"])
except:
    sys.stdout.write("Cannot connect to server\n")
    exit()

remote = XenRemote.Vmcontrol(session)
xshost = XenRemote.Hostcontrol(session)

while(True):
    # interactive console
    action = raw_input('xenremote >> ')

    # start a virtual machine
    if action=='start':
        if remote.get_stopped_vms():
            remote.get_stopped_vms_list()
            uuid = raw_input('uuid >> ')
            if remote.start_vm_by_uuid(uuid):
                sys.stdout.write("vm started\n")
            else:
                sys.stderr.write("vm cannot be started\n")
        else:
            sys.stderr.write("all vms running\n")
        continue

    # start all virtual machines
    if action=='startall':
        # we want to start all vms with this command even halted and paused ones
        # so get_stopped_vms returns a list of all non-running vms
        if remote.get_stopped_vms():
            remote.get_stopped_vms_list()
            remote.start_vms()
        else:
            sys.stderr.write("all vms running\n")

    # shutdown a virtual machine
    elif action=='shutdown':
        # we also want to clean shutdown running, paused and suspended machines
        if remote.get_running_vms() or remote.get_suspended_vms() or remote.get_paused_vms():
            remote.get_running_vms_list()
            remote.get_suspended_vms_list()
            remote.get_paused_vms_list()
            uuid = raw_input('uuid >> ')
            if remote.shutdown_vm_by_uuid(uuid):
                sys.stdout.write("vm stopped\n")
            else:
                sys.stderr.write("vm cannot be stopped\n")
        else:
            sys.stderr.write("all vms halted\n")
        continue

    # shutdown all virtual machines
    elif action=='shutdownall':
        if remote.get_running_vms() or remote.get_suspended_vms() or remote.get_paused_vms():
            remote.get_running_vms_list()
            remote.get_suspended_vms_list()
            remote.get_paused_vms_list()
            remote.shutdown_vms()
        else:
            print('all vms halted')

    # suspend a virtual machine
    elif action=='suspend':
        if remote.get_running_vms():
            remote.get_running_vms_list()
            uuid = raw_input('uuid >> ')
            if remote.suspend_vm_by_uuid(uuid):
                sys.stdout.write("vm suspended\n")
            else:
                sys.stderr.write("vm cannot be suspended\n")
        else:
            sys.stderr.write("all vms halted, suspended or paused\n")
        continue

    # pause a virtual machine
    elif action=='pause':
        if remote.get_running_vms():
            remote.get_running_vms_list()
            uuid = raw_input('uuid >> ')
            if remote.pause_vm_by_uuid(uuid):
                sys.stdout.write("vm paused\n")
            else:
                sys.stderr.write("vm cannot be paused\n")
        else:
            sys.stderr.write("all vms halted, suspended or paused\n")
        continue

    # show the status of all virtual machines
    elif action=='status':
        remote.get_vms_list()

    # show help options
    elif action=='help':
        sys.stdout.write("XenRemote (C) 2014 W. Babernits <wbabernits@onenext.de>\n\n")
        sys.stdout.write("available commands:\nstart, startall, shutdown, shutdownall, suspend, pause, status, help, version, exit\n\n")

    # print xenremote version
    elif action=='version':
        print("{0}/{1}-{2}".format(name, version, level))

    # exit program
    elif action=='exit':
        sys.stdout.write("terminated by user\n")
        exit()

    # unknown command
    else:
        sys.stderr.write("unknown command: type help for a list of available commands\n")
