# XenServer XAPI CL interface
#
# (C) 2014 Wilhelm Babernits <wbabernits@onenext.de>
# Steuert XenServer ueber die verfuegbare XAPI und verwendet die XenAPI Klasse
# um darauf zuzugreifen

import time


# Kontrolliert die virtuellen Maschinen und liest Informationen aus
class Vmcontrol(object):
    def __init__(self, session):
        self.session = session

    def get_vm_status_list(self):
        """
        Holt eine Liste aller verfuegbaren VMs der Session vom XenServer Host und gibt die UUID sowie den Status aus
        """
        vms = self.session.xenapi.VM.get_all()
        for vm in vms:
            record = self.session.xenapi.VM.get_record(vm)
            if not(record["is_a_template"]) and not(record["is_control_domain"]):
                print(record["uuid"] + " - " + record["name_label"] + " - " + record["power_state"])

    def get_running_vm_list(self):
        """
        Holt eine Liste aller laufenden VMs der Session vom XenServer Host und gibt die UUID sowie den Status aus
        """
        vms = self.session.xenapi.VM.get_all()
        for vm in vms:
            record = self.session.xenapi.VM.get_record(vm)
            if (not record["is_a_template"] and not record["is_control_domain"]) and record["power_state"]=="Running":
                print(record["uuid"] + " - " + record["name_label"] + " - " + record["power_state"])

    def get_halted_vm_list(self):
        """
        Holt eine Liste aller laufenden VMs der Session vom XenServer Host und gibt die UUID sowie den Status aus
        """
        vms = self.session.xenapi.VM.get_all()
        for vm in vms:
            record = self.session.xenapi.VM.get_record(vm)
            if (not record["is_a_template"] and not record["is_control_domain"]) and record["power_state"]=="Halted":
                print(record["uuid"] + " - " + record["name_label"] + " - " + record["power_state"])

    def get_suspended_vm_list(self):
        """
        Holt eine Liste aller laufenden VMs der Session vom XenServer Host und gibt die UUID sowie den Status aus
        """
        vms = self.session.xenapi.VM.get_all()
        for vm in vms:
            record = self.session.xenapi.VM.get_record(vm)
            if (not record["is_a_template"] and not record["is_control_domain"]) and record["power_state"]=="Suspended":
                print(record["uuid"] + " - " + record["name_label"] + " - " + record["power_state"])

    def get_paused_vm_list(self):
        """
        Holt eine Liste aller laufenden VMs der Session vom XenServer Host und gibt die UUID sowie den Status aus
        """
        vms = self.session.xenapi.VM.get_all()
        for vm in vms:
            record = self.session.xenapi.VM.get_record(vm)
            if (not record["is_a_template"] and not record["is_control_domain"]) and record["power_state"]=="Paused":
                print(record["uuid"] + " - " + record["name_label"] + " - " + record["power_state"])

    def get_vm_status_by_uuid(self, uuid):
        """
        Gibt den aktuellen Status der VM anhand der UUID zurueck
        @param uuid:
        @return:
        """
        record = self.session.xenapi.VM.get_record(self.session.xenapi.VM.get_by_uuid(uuid))
        return record["power_state"]

    def shutdown_vm_by_uuid(self, uuid):
        """
        Stoppt eine VM anhand der UUID
        @param uuid:
        """
        vm = self.session.xenapi.VM.get_by_uuid(uuid)
        record = self.session.xenapi.VM.get_record(vm)
        if record["power_state"] == "Suspended":
            self.session.xenapi.VM.resume(vm, False, True)
            time.sleep(3.0)
            self.session.xenapi.VM.clean_shutdown(vm)
        elif record["power_state"] == "Paused":
            self.session.xenapi.VM.unpause(vm)
            self.session.xenapi.VM.clean_shutdown(vm)
        elif record["power_state"] == "Running":
            self.session.xenapi.VM.clean_shutdown(vm)

        if(self.get_vm_status_by_uuid(uuid)=="Halted"):
            return True
        else:
            return False

    def start_vm_by_uuid(self, uuid):
        """
        Startet eine VM anhand der UUID
        @param uuid:
        """
        vm = self.session.xenapi.VM.get_by_uuid(uuid)
        record = self.session.xenapi.VM.get_record(vm)
        if record["power_state"] == "Suspended":
            self.session.xenapi.VM.resume(vm, False, True)
        elif record["power_state"] == "Paused":
            self.session.xenapi.VM.unpause(vm)
        elif record["power_state"] == "Halted":
            self.session.xenapi.VM.start(vm, False, True)

        if(self.get_vm_status_by_uuid(uuid)=="Running"):
            return True
        else:
            return False

    def suspend_vm_by_uuid(self, uuid):
        """
        Schickt eine VM anhand der UUID in den Schlafzustand
        @param uuid:
        """
        vm = self.session.xenapi.VM.get_by_uuid(uuid)
        record = self.session.xenapi.VM.get_record(vm)
        if record["power_state"] == "Running":
            self.session.xenapi.VM.suspend(vm)

        if(self.get_vm_status_by_uuid(uuid)=="Suspended"):
            return True
        else:
            return False

    def pause_vm_by_uuid(self, uuid):
        """
        Pausiert eine VM anhand der UUID
        @param uuid:
        """
        vm = self.session.xenapi.VM.get_by_uuid(uuid)
        record = self.session.xenapi.VM.get_record(vm)
        if record["power_state"] == "Running":
            self.session.xenapi.VM.pause(vm)
        elif record["power_state"] == "Suspended":
            self.session.xenapi.VM.resume(vm, False, True)
            self.session.xenapi.VM.pause(vm)

        if(self.get_vm_status_by_uuid(uuid)=="Paused"):
            return True
        else:
            return False

    def unpause_vm_by_uuid(self, uuid):
        """
        Unterbricht die Pause einer VM anhand der UUID
        @param uuid:
        """
        vm = self.session.xenapi.VM.get_by_uuid(uuid)
        record = self.session.xenapi.VM.get_record(vm)
        if record["power_state"] == "Paused":
            self.session.xenapi.VM.unpause(vm)

        if(self.get_vm_status_by_uuid(uuid)=="Running"):
            return True
        else:
            return False

# Steuert den XenServer Host
class Hostcontrol(object):
    def __init__(self, session):
        self.session = session
