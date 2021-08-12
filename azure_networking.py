import azure_networking_base
import client_handlers
import static_handler_utils
import logging
from msrestazure.azure_exceptions import  CloudError
logging.getLogger().setLevel(logging.INFO)


class BuildNetwork(azure_networking_base.BaseAzure):
    def __init__(self,subscription_id,vnet_name):
        super(BuildNetwork, self).__init__(subscription_id)
        self.vnet_name = vnet_name

    def build_virtual_network(self,resource_group_name,address_prefix,location):
        try:
            is_network_exist = False
            addr_list = []
            cred_object = static_handler_utils.StaticHandlers.read_secret()
            credential = client_handlers.ClientHandlers.login_to_azure(**cred_object)
            for i in self.list_all_vnet():
                if i[1] == self.vnet_name:
                    logging.info(i[1])
                    is_network_exist = True
            if not is_network_exist:
                addr_list.append(str(address_prefix))
                for i in addr_list:
                    virtual_network = client_handlers.ClientHandlers.get_network_client(credential, self.subscription_id). \
                        virtual_networks. \
                        create_or_update(resource_group_name=resource_group_name, virtual_network_name=self.vnet_name,
                                         parameters={'location': location,
                                                     'address_space': {'address_prefixes': i}})
                    return virtual_network.__dict__['_response'].json()
            else:
                return client_handlers.ClientHandlers.static_reply()

        except CloudError as e:
            logging.error(e.message)

    def build_nsg(self,subnet_name,resource_group,location):
        try:
            nsg_name = "nsg"+'-'+subnet_name
            cred_object = static_handler_utils.StaticHandlers.read_secret()
            credential = client_handlers.ClientHandlers.login_to_azure(**cred_object)
            parameter = client_handlers.ClientHandlers.create_nsg_object()
            parameter.location = location
            nsg = client_handlers.ClientHandlers.get_network_client(credential, self.subscription_id).\
                                    network_security_groups.\
                                    create_or_update(resource_group_name=resource_group,network_security_group_name=nsg_name,parameters=parameter)
            return nsg.result()

        except CloudError as e:
            logging.error(e.message)

    def build_subnet(self,subnet_name,cidr,location):
        try :
            flag = False
            cred_object = static_handler_utils.StaticHandlers.read_secret()
            credential = client_handlers.ClientHandlers.login_to_azure(**cred_object)
            vnet_address = self.get_vnet_details(self.vnet_name)[0][0]
            print(vnet_address)
            rg_name = self.get_vnet_resource_group(vnet_name=self.vnet_name)
            subnet_fulname = subnet_name+'-'+self.vnet_name
            subnet_addr = static_handler_utils.StaticHandlers.break_ip_range(vnet_address, int(cidr))   # #returning a list of IPs which are /cidr in range
            print(len(subnet_addr))
            network_security_group = self.build_nsg(subnet_name=subnet_fulname, resource_group=rg_name,
                                                    location=location)
            for i in self.get_vnet_details(self.vnet_name)[1]:
                print (i[1])
                if i[1] == subnet_fulname:
                    flag = True
                    print('subnet exist')

            if not flag:
                for i in subnet_addr:
                    try:
                        print(i)
                        parameters = client_handlers.ClientHandlers.create_subnet_object(address_prefix=i,nsg=network_security_group)
                        print(parameters)
                        subnet = client_handlers.ClientHandlers.get_network_client(credential, self.subscription_id). \
                            subnets.create_or_update(resource_group_name=rg_name, subnet_name=subnet_fulname,
                                                     virtual_network_name=self.vnet_name,
                                                     subnet_parameters=parameters)         # iterate through the list if exception happens  it should go to next

                        if type(subnet):
                            return [i]
                        break

                    except CloudError as e:
                        print(str(e.message))
            else :
                return client_handlers.ClientHandlers.static_reply()[1]

        except CloudError as e:
            logging.error(e.message)

    def connect_vnet(self,remote_vnet):
        try:
            cred_object = static_handler_utils.StaticHandlers.read_secret()
            credential = client_handlers.ClientHandlers.login_to_azure(**cred_object)

            flag = False
            for i in self.get_peering_networks(self.vnet_name):
                print(i)
                if i == remote_vnet:
                    flag = True

            if not flag:
                rg_vnet = self.get_vnet_resource_group(self.vnet_name)
                resource_details = client_handlers.ClientHandlers.get_resource_client(credential, self.subscription_id).resources.get(rg_vnet,"Microsoft.Network", "", "virtualNetworks", self.vnet_name, "2017-06-01")
                res_Id = client_handlers.ClientHandlers.generating_resource_id(resource_details)
                print(res_Id)
                rg_remote_vnet = self.get_vnet_resource_group(remote_vnet)
                target_resource_details = client_handlers.ClientHandlers.get_resource_client(credential, self.subscription_id).resources.get(rg_remote_vnet,"Microsoft.Network", "", "virtualNetworks", remote_vnet, "2017-06-01")
                target_res_id = client_handlers.ClientHandlers.generating_resource_id(target_resource_details)
                vnet_param = client_handlers.ClientHandlers.create_peering_object(res_Id)
                remote_vnet_param = client_handlers.ClientHandlers.create_peering_object(target_res_id)
                logging.info(vnet_param)
                logging.info(remote_vnet_param)
                logging.info(self.vnet_name)
                client_handlers.ClientHandlers.get_network_client(credential, self.subscription_id)\
                                                .virtual_network_peerings.create_or_update(rg_remote_vnet, remote_vnet, remote_vnet+'-to-'+self.vnet_name,
                                                                                           vnet_param)

                client_handlers.ClientHandlers.get_network_client(credential, self.subscription_id)\
                                                .virtual_network_peerings.create_or_update(rg_vnet, self.vnet_name, self.vnet_name+'-to-'+remote_vnet,remote_vnet_param )
                return client_handlers.ClientHandlers.static_reply()[2]
            else:
                return client_handlers.ClientHandlers.static_reply()[1]

        except CloudError as e:
            logging.error(e.message)

