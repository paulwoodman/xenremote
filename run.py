#!/usr/bin/env python

# XenServer XAPI CL interface
#
# (C) 2015 Wilhelm Babernits <wbabernits@onenext.de>

import sys
import readline
import XenAPI
import XenRemote

# unused at the moment
#import argparse

from subprocess import call
from configobj import ConfigObj


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

name = 'XenRemote'
version = '0.0.3'
release = '1'

conf = ConfigObj("xenremote.conf")

session = XenAPI.Session(conf["url"])

try:
    session.xenapi.login_with_password(conf["user"], conf["pass"])
except:
    sys.stdout.write("cannot connect to server\n")
    exit()

remote = XenRemote.Vmcontrol(session)
xshost = XenRemote.Hostcontrol(session)

commands = ['start', 'startall', 'shutdown', 'shutdownall', 'suspend', 'pause', 'status', 'dmesg', 'help', 'version', 'details', 'clear', 'exit']

def completer(text, state):
    options = [x for x in commands if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

while(True):
    # interactive console
    action = raw_input(color.BLUE + 'xenremote >> ' + color.END)

    # start a virtual machine
    if action=='start':
        if remote.get_stopped_vms():
            remote.get_stopped_vms_list()
            uuid = raw_input(color.BLUE + 'uuid >> ' + color.END)
            if not uuid:
                sys.stderr.write(color.RED + "missing uuid\n" + color.END)
                continue
            if remote.start_vm_by_uuid(uuid):
                sys.stdout.write(color.GREEN + "vm started\n" + color.END)
            else:
                sys.stderr.write(color.RED + "vm cannot be started\n" + color.END)
        else:
            sys.stderr.write(color.YELLOW + "all vms running\n" + color.END)
        continue

    # start all virtual machines
    if action=='startall':
        # we want to start all vms with this command even halted and paused ones
        # so get_stopped_vms returns a list of all non-running vms
        if remote.get_stopped_vms():
            remote.get_stopped_vms_list()
            remote.start_vms()
        else:
            sys.stderr.write(color.YELLOW + "all vms running\n" + color.END)

    # get the detailed status of a running virtual machine
    elif action=='details':
        # details should be available for all vms so we can easily use get_vms_list here
        remote.get_vms_list()
        uuid = raw_input(color.BLUE + 'uuid >> ' + color.END)
        if not uuid:
            sys.stderr.write(color.RED + "missing uuid\n" + color.END)
            continue
        print remote.get_vm_details_by_uuid(uuid)

    # shutdown a virtual machine
    elif action=='shutdown':
        # we also want to clean shutdown running, paused and suspended machines
        if remote.get_running_vms() or remote.get_suspended_vms() or remote.get_paused_vms():
            remote.get_suspended_vms_list()
            remote.get_paused_vms_list()
            remote.get_running_vms_list()
            uuid = raw_input(color.BLUE + 'uuid >> ' + color.END)
            if not uuid:
                sys.stderr.write(color.RED + "missing uuid\n" + color.END)
                continue
            if remote.shutdown_vm_by_uuid(uuid):
                sys.stdout.write(color.GREEN + "vm stopped\n" + color.END)
            else:
                sys.stderr.write(color.RED + "vm cannot be stopped\n" + color.END)
        else:
            sys.stderr.write(color.YELLOW + "all vms halted\n" + color.END)
        continue

    # shutdown all virtual machines
    elif action=='shutdownall':
        if remote.get_running_vms() or remote.get_suspended_vms() or remote.get_paused_vms():
            remote.get_suspended_vms_list()
            remote.get_paused_vms_list()
            remote.get_running_vms_list()
            remote.shutdown_vms()
        else:
            print(color.YELLOW + 'all vms halted' + color.END)

    # suspend a virtual machine
    elif action=='suspend':
        if remote.get_running_vms():
            remote.get_running_vms_list()
            uuid = raw_input(color.BLUE + 'uuid >> ' + color.END)
            if not uuid:
                sys.stderr.write(color.RED + "missing uuid\n" + color.END)
                continue
            if remote.suspend_vm_by_uuid(uuid):
                sys.stdout.write(color.GREEN + "vm suspended\n" + color.END)
            else:
                sys.stderr.write(color.RED + "vm cannot be suspended\n" + color.END)
        else:
            sys.stderr.write(color.YELLOW + "all vms halted, suspended or paused\n" + color.END)
        continue

    # pause a virtual machine
    elif action=='pause':
        if remote.get_running_vms():
            remote.get_running_vms_list()
            uuid = raw_input(color.BLUE + 'uuid >> ' + color.END)
            if not uuid:
                sys.stderr.write(color.RED + "missing uuid\n" + color.END)
                continue
            if remote.pause_vm_by_uuid(uuid):
                sys.stdout.write(color.GREEN + "vm paused\n" + color.END)
            else:
                sys.stderr.write(color.RED + "vm cannot be paused\n" + color.END)
        else:
            sys.stderr.write(color.YELLOW + "all vms halted, suspended or paused\n" + color.END)
        continue

    # show the status of all virtual machines
    elif action=='status':
        remote.get_vms_list()

    # get the host dmesg output
    elif action=='dmesg':
        print remote.get_dmesg()

    # show help options
    elif action=='help':
        sys.stdout.write(name + " CLI (C) 2014-2015 W. Babernits <wbabernits@onenext.de>\n\n")
        sys.stdout.write("available commands:\n\n")
        commands = sorted(commands)
        for command in commands:
            sys.stdout.write("  " + command + "\n")
        sys.stdout.write("\n")

    # print xenremote version
    elif action=='version':
        print("{0}/{1}-{2}".format(name, version, release))
        remote.get_version()

    # clear the terminal screen
    elif action=='clear':
        call(["clear"])

    # exit program
    elif action=='exit':
        sys.stdout.write("terminated by user\n")
        exit()

    # unknown command
    else:
        sys.stderr.write("unknown command: type help for a list of available commands\n")
