import static_handler_utils
from client_handlers import ClientHandlers
import logging
from msrestazure.azure_exceptions import  CloudError
logging.getLogger().setLevel(logging.INFO)


class BaseAzure:    # Base class should contain all the  get and helper function

    def __init__(self,subscription_id):
        self.subscription_id = subscription_id

    def list_all_vnet(self):       # Fetching details of all virtual network in subscription
        try:
            cred_object = static_handler_utils.StaticHandlers.read_secret()
            credential = ClientHandlers.login_to_azure(**cred_object)
            network_list = []
            final_list = []
            for element in ClientHandlers.get_network_client(credential,
                                        self.subscription_id).virtual_networks.list_all():

                network_list.append(element)
            if len(network_list) > 0:
                for network in network_list:
                    final_list.append((network.__dict__['id'], network.__dict__['name'],
                                   network.__dict__['address_space'].__dict__['address_prefixes'][0]))
                return final_list
            else:
                return ClientHandlers.static_reply()

        except CloudError as e:
            logging.error((str(e)))

    def getting_vnet_id(self,vnet_name):
        try:
            vnet_list = self.list_all_vnet()
            for i in vnet_list:
                if i[1] == vnet_name:
                    return i[0]
        except CloudError as e :
            logging.error(str(e))

    def get_vnet_resource_group(self, vnet_name):
        try:
            for i in self.list_all_vnet():  # provides Id of each virtual network
                if (i[0].split('/')[8]) == vnet_name:
                    return i[0].split('/')[4]       # getting resource group name
        except CloudError as e:
            logging.error(e)

    def get_peering_networks(self,vnet_name):
        try:
            peering_list = []
            cred_object = static_handler_utils.StaticHandlers.read_secret()
            credential = ClientHandlers.login_to_azure(**cred_object)
            rg_name  = self.get_vnet_resource_group(vnet_name)     # getting resource group for virtual network
            if rg_name != None:
                peering_object = ClientHandlers.get_network_client(credential,
                                                    self.subscription_id).virtual_network_peerings.list(
                                                    resource_group_name=rg_name, virtual_network_name=vnet_name)

                for i in peering_object:
                    peering_list.append(i.__dict__['id'].split('/')[10].split('-to-')[1])

            if len(peering_list) > 0:
                return peering_list
            else:
                return ClientHandlers.static_reply()
        except CloudError as e:
            logging.error(e)

    def get_vnet_details(self,vnet_name):
        try:
            cred_object = static_handler_utils.StaticHandlers.read_secret()
            credential = ClientHandlers.login_to_azure(**cred_object)
            rg_name = self.get_vnet_resource_group(vnet_name)
            if rg_name != None :
                subnet_det = []
                virtual_network = ClientHandlers.get_network_client(credential,
                                self.subscription_id).virtual_networks.get(
                    resource_group_name=rg_name, virtual_network_name=vnet_name).__dict__

                subnet_details = virtual_network['subnets']
                for subnet in subnet_details:
                    subnet_det.append((subnet.__dict__['address_prefix'], subnet.__dict__['id'].split('/')[10]))

                return [virtual_network['address_space'].__dict__['address_prefixes'], subnet_det]
            else :
                return ClientHandlers.static_reply()
        except CloudError as e:
            logging.error(e)

    def get_network_interface(self,nic_id):
        try:
            network_interface_details = {}
            nic_name = nic_id.split('/')[-1]
            rg_name = nic_id.split('/')[4]
            cred_object = static_handler_utils.StaticHandlers.read_secret()
            credential = ClientHandlers.login_to_azure(**cred_object)
            network_interface = ClientHandlers.get_network_client(credential,self.subscription_id).network_interfaces.\
                get(resource_group_name=rg_name,network_interface_name=nic_name)
            for nic in network_interface.ip_configurations:
                network_interface_details['subnet_id'] = nic.subnet.id
                network_interface_details["private_ip"] = nic.private_ip_address
                if nic.public_ip_address is None:
                    network_interface_details["public_ip"] = nic.public_ip_address
                else:
                    public_ip = nic.public_ip_address.__dict__
                    id = public_ip['id']
                    public_ip_name = id.split('/')[-1]
                    public_rg_name = id.split('/')[4]
                    public_ip_details = ClientHandlers.get_network_client(credential, self.subscription_id).\
                        public_ip_addresses.\
                        get(resource_group_name= public_rg_name ,public_ip_address_name= public_ip_name)
                    network_interface_details["public_ip"] = public_ip_details.__dict__['ip_address']

            return network_interface_details
        except CloudError as e:
            logging.error(e)

    def get_subnet_details(self,subnet_id):
        try:
            subnet_details =[]
            vnet_rg_name = subnet_id.split('/')[4]
            vnet_name = subnet_id.split('/')[8]
            subnet_name = subnet_id.split('/')[10]
            cred_object = static_handler_utils.StaticHandlers.read_secret()
            credential = ClientHandlers.login_to_azure(**cred_object)
            subnet = ClientHandlers.get_network_client(credential,self.subscription_id).subnets.get(resource_group_name=vnet_rg_name,virtual_network_name= vnet_name, subnet_name=subnet_name)
            logging.info(subnet)
            subnet_details.append(subnet.name)
            subnet_details.append(subnet.address_prefix)
            if subnet.__dict__['network_security_group'] is None:
                logging.warning("! No NSG in subnet  ")
                subnet_details.append(subnet.__dict__['network_security_group'])
            else:
                nsg_id = subnet.__dict__['network_security_group'].id
                subnet_details.append(nsg_id.split('/')[-1])

            return subnet_details

        except CloudError as e:
            logging.error(e)


