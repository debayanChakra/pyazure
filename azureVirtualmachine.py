import Networkpy
import ResourceGroup
from azure.mgmt.compute import ComputeManagementClient


class azureVirtualmachine:
    def __init__(self,credential,subscriptionId):
        self.credential=credential
        self.subscriptionId=subscriptionId

    def creating_compute_management_client(self):
        return ComputeManagementClient(credentials=self.credential,subscription_id= self.subscriptionId)

    def geting_details_of_virtualmachine_in_subscription(self,ResourcegroupName,vmname):
        client =self.creating_compute_management_client()
        virtual_machine = client.virtual_machines.get(resource_group_name=ResourcegroupName,vm_name=vmname)
        storage_profile={}

        #return virtual_machine.provisioning_state
        managed_disk={}
        #return virtual_machine.storage_profile
        managed_disk['id']=virtual_machine.storage_profile.os_disk.managed_disk.id
        managed_disk['storage_account_type'] =virtual_machine.storage_profile.os_disk.managed_disk.storage_account_type
        os_disk={}
        os_disk["managed_disk"]=managed_disk
        os_disk['disk_size_gb']=virtual_machine.storage_profile.os_disk.disk_size_gb
        os_disk['disk_name']=virtual_machine.storage_profile.os_disk.name
        os_disk['create_option']=virtual_machine.storage_profile.os_disk.create_option
        os_disk['encryption_settings']=virtual_machine.storage_profile.os_disk.encryption_settings
        #return os_disk
        data_disks =[]
        data_disk_detail= virtual_machine.storage_profile.data_disks
        for data in data_disk_detail:
            data_disk={}

            managed_disk =data.managed_disk.__dict__
            data_disk['managed_disk']=managed_disk
            data_disk['disk_size_gb'] = data.disk_size_gb
            data_disk['disk_name'] = data.name
            data_disk['create_option'] =data.create_option

            data_disk['lun'] = data.lun
            data_disks.append(data_disk)

        image_reference =virtual_machine.storage_profile.image_reference
        image={}
        image_reference= image_reference.__dict__
        image["image_reference"]=image_reference

        storage_profile['os_disk']=os_disk
        storage_profile['data_disks']=data_disks
        storage_profile['image_reference']=image

        Network_profile=[]
        Network_profiles = virtual_machine.network_profile.network_interfaces
        for network in Network_profiles:
            network_interfaces={}
            network_interface= network.__dict__
            network_interfaces['network_interfaces']=network_interface
            Network_profile.append(network_interfaces)
        hardware_profile =virtual_machine.hardware_profile
        hardware_profile= hardware_profile.__dict__
        tags=virtual_machine.tags
        diagnostics_profile=virtual_machine.diagnostics_profile.boot_diagnostics.__dict__


        virtual_machine_detail={}

        virtual_machine_detail['storage_profile']=storage_profile
        virtual_machine_detail['network_profile']=Network_profile
        virtual_machine_detail['tags']=tags
        virtual_machine_detail['hardware_profile']=hardware_profile
        virtual_machine_detail['provisioning_state']=virtual_machine.provisioning_state


        virtual_machine_detail['id']=virtual_machine.id
        virtual_machine_detail['type']=virtual_machine.type
        virtual_machine_detail['location']=virtual_machine.location
        virtual_machine_detail['diagnostics_profile']=diagnostics_profile
        return virtual_machine_detail

    def start_virtualmachine(self,vmname,ResourceGroupName):
        client=self.creating_compute_management_client()
        status_vm =client.virtual_machines.start(resource_group_name=ResourceGroupName,vm_name=vmname)
        return status_vm
    def stop_virtualmachine(self,vmname,ResourceGroupName):
        client=self.creating_compute_management_client()
        status_vm=client.virtual_machines.deallocate(resource_group_name=ResourceGroupName,vm_name=vmname)
        return status_vm
    def resizing_virtual_machine(self,vmname,ResourceGroupName,Desired_size):
        client=self.creating_compute_management_client()
        vm_size=client.virtual_machines.create_or_update()
