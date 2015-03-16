#!/usr/bin/env python

# XenServer XAPI CL interface
#
# (C) 2015 Wilhelm Babernits <wbabernits@onenext.de>

import sys
import readline
import XenAPI
import XenRemote
from termcolor import colored, cprint
from subprocess import call
from configobj import ConfigObj


name = 'XenRemote'
version = '0.0.3'
release = '1'

conf = ConfigObj("xenremote.conf")

session = XenAPI.Session(conf["url"])

try:
    session.xenapi.login_with_password(conf["user"], conf["pass"])
except:
    sys.stdout.write(colored("cannot connect to server\n", "red"))
    exit()

remote = XenRemote.Vmcontrol(session)
xshost = XenRemote.Hostcontrol(session)

# tab completion
commands = ['start', 'startall', 'shutdown', 'shutdownall', 'suspend', 'pause', 'status', 'dmesg', 'help', 'version', 'details', 'clear', 'exit']

def completer(text, state):
    options = [x for x in commands if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

# loop
while(True):
    # interactive console
    action = raw_input(colored('xenremote >> ', 'cyan'))

    # start a virtual machine
    if action=='start':
        if remote.get_stopped_vms():
            remote.get_stopped_vms_list()
            uuid = raw_input(colored('uuid >> ', 'cyan'))
            if not uuid:
                sys.stderr.write(colored("missing uuid\n", "red"))
                continue
            if remote.start_vm_by_uuid(uuid):
                sys.stdout.write(colored("vm started\n", "green"))
            else:
                sys.stderr.write(colored("vm cannot be started\n", "red"))
        else:
            sys.stderr.write(colored("all vms running\n", "yellow"))
        continue

    # start all virtual machines
    if action=='startall':
        # we want to start all vms with this command even halted and paused ones
        # so get_stopped_vms returns a list of all non-running vms
        if remote.get_stopped_vms():
            remote.get_stopped_vms_list()
            remote.start_vms()
        else:
            sys.stderr.write(colored("all vms running\n", "yellow"))

    # get the detailed status of a running virtual machine
    elif action=='details':
        # details should be available for all vms so we can easily use get_vms_list here
        remote.get_vms_list()
        uuid = raw_input(colored('uuid >> ', 'cyan'))
        if not uuid:
            sys.stderr.write(colored("missing uuid\n", "red"))
            continue
        print remote.get_vm_details_by_uuid(uuid)

    # shutdown a virtual machine
    elif action=='shutdown':
        # clean shutdown of running, paused and suspended machines
        if remote.get_running_vms() or remote.get_suspended_vms() or remote.get_paused_vms():
            remote.get_suspended_vms_list()
            remote.get_paused_vms_list()
            remote.get_running_vms_list()
            uuid = raw_input(colored('uuid >> ', 'cyan'))
            if not uuid:
                sys.stderr.write(colored("missing uuid\n", "red"))
                continue
            if remote.shutdown_vm_by_uuid(uuid):
                sys.stdout.write(colored("vm stopped\n", "green"))
            else:
                sys.stderr.write(colored("vm cannot be stopped\n", "red"))
        else:
            sys.stderr.write(colored("all vms halted\n", "yellow"))
        continue

    # shutdown all virtual machines
    elif action=='shutdownall':
        if remote.get_running_vms() or remote.get_suspended_vms() or remote.get_paused_vms():
            remote.get_suspended_vms_list()
            remote.get_paused_vms_list()
            remote.get_running_vms_list()
            remote.shutdown_vms()
        else:
            print(colored('all vms halted', 'yellow'))

    # suspend a virtual machine
    elif action=='suspend':
        if remote.get_running_vms():
            remote.get_running_vms_list()
            uuid = raw_input(colored('uuid >> ', 'cyan'))
            if not uuid:
                sys.stderr.write(colored("missing uuid\n", "red"))
                continue
            if remote.suspend_vm_by_uuid(uuid):
                sys.stdout.write(colored("vm suspended\n", "green"))
            else:
                sys.stderr.write(colored("vm cannot be suspended\n", "red"))
        else:
            sys.stderr.write(colored("all vms halted, suspended or paused\n", "yellow"))
        continue

    # pause a virtual machine
    elif action=='pause':
        if remote.get_running_vms():
            remote.get_running_vms_list()
            uuid = raw_input(colored('uuid >> ', 'cyan'))
            if not uuid:
                sys.stderr.write(colored("missing uuid\n", "red"))
                continue
            if remote.pause_vm_by_uuid(uuid):
                sys.stdout.write(colored("vm paused\n", "green"))
            else:
                sys.stderr.write(colored("vm cannot be paused\n", "red"))
        else:
            sys.stderr.write(colored("all vms halted, suspended or paused\n", "yellow"))
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
        for command in sorted(commands):
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
