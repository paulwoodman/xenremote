# XenServer XAPI CL interface class
#
# (C) 2014 Wilhelm Babernits <wbabernits@onenext.de>

import time


class Vmcontrol(object):
    def __init__(self, session):
        self.session = session

    def get_vm_status_list(self):
        """
        Get current power_state and UUIDs of all VMs as a hr list
        """
        vms = self.session.xenapi.VM.get_all()
        for vm in vms:
            record = self.session.xenapi.VM.get_record(vm)
            if not record["is_a_template"] and not record["is_control_domain"]:
                print(record["uuid"] + " - " + record["name_label"] + " - " + record["power_state"])

    def get_running_vm_list(self):
        """
        Get running VMs as a hr list
        """
        vms = self.session.xenapi.VM.get_all()
        for vm in vms:
            record = self.session.xenapi.VM.get_record(vm)
            if (not record["is_a_template"] and not record["is_control_domain"]) and record["power_state"] == "Running":
                print(record["uuid"] + " - " + record["name_label"] + " - " + record["power_state"])

    def get_halted_vm_list(self):
        """
        Get halted VMs as a hr list
        """
        vms = self.session.xenapi.VM.get_all()
        for vm in vms:
            record = self.session.xenapi.VM.get_record(vm)
            if (not record["is_a_template"] and not record["is_control_domain"]) and record["power_state"] == "Halted":
                print(record["uuid"] + " - " + record["name_label"] + " - " + record["power_state"])

    def get_suspended_vm_list(self):
        """
        Get suspended VMs as a hr list
        """
        vms = self.session.xenapi.VM.get_all()
        for vm in vms:
            record = self.session.xenapi.VM.get_record(vm)
            if (not record["is_a_template"] and not record["is_control_domain"]) and record[
                "power_state"] == "Suspended":
                print(record["uuid"] + " - " + record["name_label"] + " - " + record["power_state"])

    def get_paused_vm_list(self):
        """
        Get paused VMs as a hr list
        """
        vms = self.session.xenapi.VM.get_all()
        for vm in vms:
            record = self.session.xenapi.VM.get_record(vm)
            if (not record["is_a_template"] and not record["is_control_domain"]) and record["power_state"] == "Paused":
                print(record["uuid"] + " - " + record["name_label"] + " - " + record["power_state"])

    def get_vm_status_by_uuid(self, uuid):
        """
        Returns the current power_state of a VM by UUID
        """
        return self.session.xenapi.VM.get_power_state(self.session.xenapi.VM.get_by_uuid(uuid))

    def shutdown_vm_by_uuid(self, uuid):
        """
        Stops a VM
        If a VM is paused or suspended it will
        be set to unpause or resume first
        """
        vm = self.session.xenapi.VM.get_by_uuid(uuid)
        record = self.session.xenapi.VM.get_record(vm)
        if record["power_state"] == "Suspended":
            self.session.xenapi.VM.resume(vm, False, True)
            time.sleep(1.0)
            self.session.xenapi.VM.clean_shutdown(vm)
        elif record["power_state"] == "Paused":
            self.session.xenapi.VM.unpause(vm)
            time.sleep(1.0)
            self.session.xenapi.VM.clean_shutdown(vm)
        elif record["power_state"] == "Running":
            self.session.xenapi.VM.clean_shutdown(vm)

        if self.get_vm_status_by_uuid(uuid) == "Halted":
            return True
        else:
            return False

    def start_vm_by_uuid(self, uuid):
        """
        Starts a VM
        This method also replaces unpause and resume
        """
        vm = self.session.xenapi.VM.get_by_uuid(uuid)
        record = self.session.xenapi.VM.get_record(vm)
        if record["power_state"] == "Suspended":
            self.session.xenapi.VM.resume(vm, False, True)
        elif record["power_state"] == "Paused":
            self.session.xenapi.VM.unpause(vm)
        elif record["power_state"] == "Halted":
            self.session.xenapi.VM.start(vm, False, True)

        if self.get_vm_status_by_uuid(uuid) == "Running":
            return True
        else:
            return False

    def suspend_vm_by_uuid(self, uuid):
        """
        Suspend a VM
        """
        vm = self.session.xenapi.VM.get_by_uuid(uuid)
        record = self.session.xenapi.VM.get_record(vm)
        if record["power_state"] == "Running":
            self.session.xenapi.VM.suspend(vm)

        if self.get_vm_status_by_uuid(uuid) == "Suspended":
            return True
        else:
            return False

    def pause_vm_by_uuid(self, uuid):
        """
        Pause a VM
        """
        vm = self.session.xenapi.VM.get_by_uuid(uuid)
        record = self.session.xenapi.VM.get_record(vm)
        if record["power_state"] == "Running":
            self.session.xenapi.VM.pause(vm)
        elif record["power_state"] == "Suspended":
            self.session.xenapi.VM.resume(vm, False, True)
            self.session.xenapi.VM.pause(vm)

        if self.get_vm_status_by_uuid(uuid) == "Paused":
            return True
        else:
            return False


# For future purpose
class Hostcontrol(object):
    def __init__(self, session):
        self.session = session
