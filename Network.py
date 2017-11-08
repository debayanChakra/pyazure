from azure.mgmt.network import NetworkManagementClient
import ResourceGroup

class azureNetworking:
    def __init__(self,credential,subscriptionId):
        self.credential=credential
        self.subscriptionId=subscriptionId
    def creating_network_client(self):
        return NetworkManagementClient(subscription_id=self.subscriptionId,credentials=self.credential)


    def create_virtual_network(self,VirtuaNetworkName,ResourceGroupName,Location,address_prefix):
        Rg_object= ResourceGroup.Azure_resourceGroup(self.credential,self.subscriptionId)
        #searching a ResourceGroup Exist or Not


        if Rg_object.find_resourcegroup(ResourceGroupName,Location) ==True:
            client =self.creating_network_client()

            parameter ={'location':Location,'address_space':{'address_prefixes':[address_prefix]}}
            virtual_network=client.virtual_networks.create_or_update(ResourceGroupName,VirtuaNetworkName,parameter)
            virtual_network.wait()
            return virtual_network
        else:
            return "No ResourceGroup! Kindly make one"



    def create_subnet(self,resourceGroupName,VnetName,SubnetName,address_prefix):
        address_space={'address_prefix':address_prefix}

        client = self.creating_network_client()
        subnet=client.subnets.create_or_update(resource_group_name=resourceGroupName,virtual_network_name=VnetName,subnet_name=SubnetName,subnet_parameters=address_space)
        subnet.wait()
        return subnet

    def Get_Vnet_information (self,Vnetname,ResourceGroupName):

        client= self.creating_network_client()
        vnetinfo= client.virtual_networks.get(resource_group_name=ResourceGroupName,virtual_network_name=Vnetname)
        return vnetinfo

        virtual_network_peerings =vnetinfo.virtual_network_peerings
        virtual_network_peerings_details=[]
        for networkpeering in virtual_network_peerings:
            remote_virtual_network_detail={}
            remote_virtual_network_detail['remote_virtual_network']= networkpeering.remote_virtual_network.__dict__
            virtual_network_peering={}
            virtual_network_peering['peering_state']=networkpeering.peering_state

            virtual_network_peering['name']=networkpeering.name
            virtual_network_peering['use_remote_gateways']=networkpeering.use_remote_gateways
            virtual_network_peering['etag']=networkpeering.etag

            virtual_network_peering['allow_forwarded_traffic']=networkpeering.allow_forwarded_traffic
            virtual_network_peering['id']=networkpeering.id
            virtual_network_peering['provisioning_state']=networkpeering.provisioning_state
            virtual_network_peering['remote_virtual_network']=remote_virtual_network_detail

            virtual_network_peerings_details.append(remote_virtual_network_detail)






        sub=[]
        for subnet in vnetinfo.subnets:
            sub.append( subnet.__dict__)
        address_space=vnetinfo.address_space
        address_prefix=address_space.address_prefixes

        vnet_det={'name':vnetinfo.name,"id":vnetinfo.id,'subnet':sub,'address_space':address_prefix,'tag':vnetinfo.tags,'provisioning_state':vnetinfo.provisioning_state,'location':vnetinfo.location,'virtual_network_peering':virtual_network_peerings_details})
        return vnet_det

    def creating_a_network_interface(self,nicname,Nicresourcegroupname,location,vnetname,subnetname,Vnetresourcegroup):
        Vnet_det= self.Get_Vnet_information(Vnetname=vnetname,ResourceGroupName=Vnetresourcegroup)
        subnets= Vnet_det[0]['subnet']
        subnetid=[]
        for sub in subnets:
            if sub['name']==subnetname:
                subnetid.append(sub['id'])
                client = self.creating_network_client()
                parameter = {'location': location,'ip_configurations': [{'name': "ipconfig", 'subnet': {'id': subnetid[0]}}]}
                nic = client.network_interfaces.create_or_update(resource_group_name=Nicresourcegroupname,
                                                                 network_interface_name=nicname, parameters=parameter)
                return nic
        else:
            print "subnet does not exist"


    def  creating_a_publicIP(self, publicIPName,ResourceGroup,location):
         client =self.creating_network_client()
         publicIP = client.public_ip_addresses.create_or_update(resource_group_name=ResourceGroup,public_ip_address_name=publicIPName,parameters={'public_ip_allocation_method':'static','ip_configurations':'null','location':location})

         return publicIP


    def getting_details_of_public_IP(self,publicIPName,ResourceGroup):
        client = self.creating_network_client()
        publicIp_details = client.public_ip_addresses.get(resource_group_name=ResourceGroup,public_ip_address_name=publicIPName)
        publicIP_address = publicIp_details.ip_address
        publicIP_id =publicIp_details.id
        publicIpdict ={}
        publicIpdict['ipaddress']=publicIP_address
        publicIpdict['id']=publicIP_id
        return publicIpdict


    def getting_details_of_NIC(self,Nicname, Nicresourcegroup):

        client = self.creating_network_client()
        Nic = client.network_interfaces.get(resource_group_name=Nicresourcegroup,network_interface_name=Nicname)


        dns =Nic.dns_settings.__dict__
        virtual_machine=Nic.virtual_machine.__dict__
        ip_configuration=Nic.ip_configurations

        ip_configuration=[]
        for i in Nic.ip_configurations:


            sub=i.subnet.__dict__

            public_ip_address=i.public_ip_address.__dict__
            ip_configurations={}
            ip_configurations['subnet']=sub
            ip_configurations['public_ip_address']=public_ip_address
            ip_configurations['private_ip_address_version']=i.private_ip_address_version
            ip_configurations['name']=i.name

            ip_configurations['id']=i.id
            ip_configurations['Isprimary']=i.primary
            ip_configurations['private_ip_allocation_method']=i.private_ip_allocation_method
            ip_configurations['load_balancer_backend_address_pools']=i.load_balancer_backend_address_pools
            ip_configurations['etag']=i.etag
            ip_configurations['load_balancer_inbound_nat_rules']=i.load_balancer_inbound_nat_rules
            ip_configuration.append(ip_configurations)

        network_security_group=Nic.network_security_group.__dict__

        network_interface={}
        network_interface['dns']=dns
        network_interface['virtual_machine']=virtual_machine
        network_interface['ip_configurations']=ip_configuration
        network_interface['name']=Nic.name
        network_interface['IsPrimary']=Nic.primary
        network_interface['enable_ip_forwarding']=Nic.enable_ip_forwarding
        network_interface['etag']=Nic.etag
        network_interface['tags']=Nic.tags
        network_interface['enable_accelerated_networking']=Nic.enable_accelerated_networking
        network_interface['provisioning_state']=Nic.provisioning_state
        network_interface['type']=Nic.type
        network_interface['network_security_group']=network_security_group
        network_interface['id']=Nic.id
        network_interface['location']=Nic.location
        network_interface['mac_address']=Nic.mac_address

        return network_interface






    def delete_network_interface(self,Nicname,Nicresourcegroup):
        client=self.creating_network_client()
        nic_details = self.getting_details_of_NIC(Nicresourcegroup=Nicresourcegroup,Nicname=Nicname)
        if nic_details['virtual_machine']=="None":
            network_interface=client.network_interfaces.delete(resource_group_name=Nicresourcegroup,network_interface_name=Nicname)
            print "deletion has started"
        else :
            print "Nic is attached to VirtualMachine"


    def delete_public_Ip(self,publicIPName,ResourceGroup):
        client=self.creating_network_client()
        try:

            publicIp_details= client.public_ip_addresses.delete(resource_group_name=ResourceGroup,public_ip_address_name=publicIPName)
            print "operation successful"
        except Exception as e:
            print e

    def peering_Vnet_in_same_location(self,Primary_VirtualNetwork,ResourceGroup_Primary_VirtualNetwork,Secondary_VirtualNetwork,ResourceGroup_Secondary_VirtualNetwork):

        client = self.creating_network_client()
        try:
            secondaryNetwork= self.Get_Vnet_information(Vnetname=Secondary_VirtualNetwork,ResourceGroupName=ResourceGroup_Secondary_VirtualNetwork)

            secondaryNetwork_id =secondaryNetwork[0]['id']
        except Exception as ex:
            print  ex
        try:
            virtual_network_peering_parameters={'remoteVirtualNetwork':{'id':secondaryNetwork_id},
                                                'allow_virtual_network_access':True,
                                                 'use_remote_gateway':False,
                                                  'allow_forwared_trafic':True



                                                }

            Connectivity = client.virtual_network_peerings.create_or_update(resource_group_name=ResourceGroup_Primary_VirtualNetwork,virtual_network_name=Primary_VirtualNetwork,virtual_network_peering_name=Primary_VirtualNetwork+"_" +"Peering"+"_"+Secondary_VirtualNetwork,virtual_network_peering_parameters=virtual_network_peering_parameters)

            print "peering is started.It might take few minutes......"
        except Exception as e:
            print  e
