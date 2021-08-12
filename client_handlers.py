import static_handler_utils

from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.network.models import VirtualNetworkPeering,Subnet,NetworkSecurityGroup,SubResource
from azure.mgmt.storage import StorageManagementClient
from datetime import datetime, timedelta
from azure.storage.common import SharedAccessSignature,ResourceTypes,AccountPermissions
from azure.cosmosdb.table.tableservice import TableService




class ClientHandlers:

    def __init__(self):
        pass

    @staticmethod
    def get_resource_client(credential,subscription_id):
        return ResourceManagementClient(credentials=credential, subscription_id=subscription_id)

    @staticmethod
    def get_network_client(credential,subscription_id):
        return NetworkManagementClient(credentials=credential, subscription_id=subscription_id)

    @staticmethod
    def get_storage_client(credential,subscription_id):
        return StorageManagementClient(credentials=credential,subscription_id=subscription_id)

    @staticmethod
    def get_computation_client(credential, subscription_id):
        return ComputeManagementClient(credentials=credential, subscription_id=subscription_id)

    @staticmethod
    def create_nsg_object():
        return NetworkSecurityGroup()

    @staticmethod
    def create_account_sas(storageName,key):
        return SharedAccessSignature(account_name=storageName,account_key=key).generate_account(services= "bfqt",\
                                    resource_types = ResourceTypes(object=True,service=True,container=True),permission = AccountPermissions(read=True,list=True),start=datetime.utcnow() ,expiry = datetime.utcnow() + timedelta(days=365))

    @staticmethod
    def create_account_admin_sas(storageName, key):
        return SharedAccessSignature(account_name=storageName, account_key=key).generate_account(services="bfqt", \
                                                                                                 resource_types=ResourceTypes(object=True,service=True,container=True),
                                                                                                 permission=AccountPermissions(read=True,list=True,write=True,delete=True,add=True,update=True,process=True,create=True),\
                                                                                                 start=datetime.utcnow(), expiry=datetime.utcnow() + timedelta(days=365))

    @staticmethod
    def generating_resource_id(resource):
        return SubResource(id=resource.id)

    @staticmethod
    def create_subnet_object(address_prefix,nsg):
        return Subnet(address_prefix=address_prefix,network_security_group =nsg)

    @staticmethod
    def get_blob_client():
        return BlobServiceClient()

    @staticmethod
    def create_peering_object(vnet_id):
        return VirtualNetworkPeering(allow_virtual_network_access=True, use_remote_gateways=False,
                                     allow_gateway_transit=False, remote_virtual_network=vnet_id)

    @staticmethod
    def login_to_azure(**kwargs):
        sp_key = kwargs['service_principle']['key']
        sp_client = kwargs['service_principle']['app_id']
        sp_tenant = kwargs['service_principle']['tenant']

        credentials = ServicePrincipalCredentials(
            client_id=sp_client,
            secret=sp_key,
            tenant=sp_tenant
        )
        return credentials

    @staticmethod
    def static_reply():
        return["not exist","already exist","completed","request accepted !!"]

    @staticmethod
    def entry_to_table(entry):
        return TableService(account_name="" ,account_key='').insert_entity(entity=entry,table_name='')

    @staticmethod
    def get_entry_from_table(subscription_id,storageName):
        return TableService(account_name="",account_key='').\
                get_entity(row_key=storageName,partition_key=subscription_id,table_name='')



