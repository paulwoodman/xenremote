# XenServer XAPI CL interface class
#
# (C) 2014 Wilhelm Babernits <wbabernits@onenext.de>

import time


class Vmcontrol(object):
    def __init__(self, session):
        self.session = session

    def get_vms_list(self):
        vms = self.get_vms()
        for vm in vms:
            print(vm)            

    def get_vms(self):
        vms = self.session.xenapi.VM.get_all()
        vmlist = []
        for vm in vms:
            record = self.session.xenapi.VM.get_record(vm)
            if not record["is_a_template"] and not record["is_control_domain"]:
                vmlist.append(record["uuid"] + " - " + record["name_label"] + " - " + record["power_state"])
        return vmlist

    def get_active_vms(self, getuuid=False):
        vms = self.session.xenapi.VM.get_all()
        vmlist = []
        for vm in vms:
            record = self.session.xenapi.VM.get_record(vm)
            if not record["is_a_template"] and not record["is_control_domain"] and (record["power_state"] == "Running" or record["power_state"] == "Suspended" or record["power_state"] == "Paused"):
                if getuuid==False:
                    vmlist.append(record["uuid"] + " - " + record["name_label"] + " - " + record["power_state"])
                else:
                    vmlist.append(record["uuid"])
        return vmlist

    def get_running_vms_list(self):
        vms = self.get_running_vms()
        for vm in vms:
            print(vm)

    def get_running_vms(self, getuuid=False):
        vms = self.session.xenapi.VM.get_all()
        vmlist = []
        for vm in vms:
            record = self.session.xenapi.VM.get_record(vm)
            if not record["is_a_template"] and not record["is_control_domain"] and record["power_state"] == "Running":
                if getuuid==False:
                    vmlist.append(record["uuid"] + " - " + record["name_label"] + " - " + record["power_state"])
                else:
                    vmlist.append(record["uuid"])
        return vmlist

    def get_stopped_vms_list(self):
        vms = self.get_stopped_vms()
        for vm in vms:
            print(vm)

    def get_stopped_vms(self, getuuid=False):
        vms = self.session.xenapi.VM.get_all()
        vmlist = []
        for vm in vms:
            record = self.session.xenapi.VM.get_record(vm)
            if not record["is_a_template"] and not record["is_control_domain"] and (record["power_state"] == "Halted" or record["power_state"] == "Suspended" or record["power_state"] == "Paused"):
                if getuuid==False:
                    vmlist.append(record["uuid"] + " - " + record["name_label"] + " - " + record["power_state"])
                else:
                    vmlist.append(record["uuid"])
        return vmlist

    def get_halted_vms_list(self):
        vms = self.get_halted_vms()
        for vm in vms:
            print(vm)

    def get_halted_vms(self, getuuid=False):
        vms = self.session.xenapi.VM.get_all()
        vmlist = []
        for vm in vms:
            record = self.session.xenapi.VM.get_record(vm)
            if not record["is_a_template"] and not record["is_control_domain"] and record["power_state"] == "Halted":
                if getuuid==False:
                    vmlist.append(record["uuid"] + " - " + record["name_label"] + " - " + record["power_state"])
                else:
                    vmlist.append(record["uuid"])
        return vmlist

    def get_suspended_vms_list(self):
        vms = self.get_suspended_vms()
        for vm in vms:
            print(vm)

    def get_suspended_vms(self, getuuid=False):
        vms = self.session.xenapi.VM.get_all()
        vmlist = []
        for vm in vms:
            record = self.session.xenapi.VM.get_record(vm)
            if not record["is_a_template"] and not record["is_control_domain"] and record["power_state"] == "Suspended":
                if getuuid==False:
                    vmlist.append(record["uuid"] + " - " + record["name_label"] + " - " + record["power_state"])
                else:
                    vmlist.append(record["uuid"])
        return vmlist

    def get_paused_vms_list(self):
        vms = self.get_paused_vms()
        for vm in vms:
            print(vm)

    def get_paused_vms(self, getuuid=False):
        vms = self.session.xenapi.VM.get_all()
        vmlist = []
        for vm in vms:
            record = self.session.xenapi.VM.get_record(vm)
            if not record["is_a_template"] and not record["is_control_domain"] and record["power_state"] == "Paused":
                if getuuid==False:
                    vmlist.append(record["uuid"] + " - " + record["name_label"] + " - " + record["power_state"])
                else:
                    vmlist.append(record["uuid"])
        return vmlist

    def get_vm_status_by_uuid(self, uuid):
        return self.session.xenapi.VM.get_power_state(self.session.xenapi.VM.get_by_uuid(uuid))

    def shutdown_vm_by_uuid(self, uuid):
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

    def shutdown_vms(self):
        uuids = self.get_active_vms(True)
        for uuid in uuids:
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
                print("VM " + uuid + " halted")
            else:
                print("VM " + uuid + " cannot be halted")

    def start_vm_by_uuid(self, uuid):
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

    def start_vms(self):
        uuids = self.get_stopped_vms(True)
        for uuid in uuids:
            vm = self.session.xenapi.VM.get_by_uuid(uuid)
            record = self.session.xenapi.VM.get_record(vm)
            if record["power_state"] == "Suspended":
                self.session.xenapi.VM.resume(vm, False, True)
            elif record["power_state"] == "Paused":
                self.session.xenapi.VM.unpause(vm)
            elif record["power_state"] == "Halted":
                self.session.xenapi.VM.start(vm, False, True)

            if self.get_vm_status_by_uuid(uuid) == "Running":
                print("VM " + uuid + " started")
            else:
                print("VM " + uuid + " cannot be started")

    def suspend_vm_by_uuid(self, uuid):
        vm = self.session.xenapi.VM.get_by_uuid(uuid)
        record = self.session.xenapi.VM.get_record(vm)
        if record["power_state"] == "Running":
            self.session.xenapi.VM.suspend(vm)

        if self.get_vm_status_by_uuid(uuid) == "Suspended":
            return True
        else:
            return False

    def pause_vm_by_uuid(self, uuid):
        vm = self.session.xenapi.VM.get_by_uuid(uuid)
        record = self.session.xenapi.VM.get_record(vm)
        if record["power_state"] == "Running":
            self.session.xenapi.VM.pause(vm)
        elif record["power_state"] == "Suspended":
            self.session.xenapi.VM.resume(vm, False, True)
            time.sleep(1.0)
            self.session.xenapi.VM.pause(vm)

        if self.get_vm_status_by_uuid(uuid) == "Paused":
            return True
        else:
            return False


class Hostcontrol(object):
    def __init__(self, session):
        self.session = session
