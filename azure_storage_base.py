import static_handler_utils
import client_handlers
import logging
from msrestazure.azure_exceptions import CloudError
logging.getLogger().setLevel(logging.INFO)

class BaseStorage:
    def __init__(self,subscription_id):
        self.subscription_id = subscription_id

    def list_storage(self):
        try:
            cred_object = static_handler_utils.StaticHandlers.read_secret()
            credential = client_handlers.ClientHandlers.login_to_azure(**cred_object)
            storage_list = []
            for storageAcc in client_handlers.ClientHandlers.\
                    get_storage_client(credential=credential,subscription_id=self.subscription_id).storage_accounts.list():
                storage_list.append(storageAcc.__dict__['id'])
            if len(storage_list) > 0:
                print('number of storage account', len(storage_list))
                return storage_list
            else:
                return client_handlers.ClientHandlers.static_reply()[0]
        except CloudError as e:
            logging.error(e)

    def find_rg_of_storage(self,storageName):
        try:
            for id in self.list_storage():
                if (id.split('/')[8]) == storageName:
                    print('storage matched!...')
                    return id.split('/')[4]

        except CloudError as e:
            logging.error(e)

    def find_key(self,storageName):
        try:
            cred_object = static_handler_utils.StaticHandlers.read_secret()
            credential = client_handlers.ClientHandlers.login_to_azure(**cred_object)
            if  self.find_rg_of_storage(storageName) :
                logging.info('storage account exist!!..')
                rgName = self.find_rg_of_storage(storageName)
                logging.info('rg name is',rgName)
                key_details=client_handlers.ClientHandlers.\
                    get_storage_client(credential=credential,subscription_id=self.subscription_id).\
                    storage_accounts.list_keys(resource_group_name=rgName,account_name=storageName)
                logging.info(key_details.__dict__['keys'])
                return (key_details.__dict__['keys'][0]).__dict__['value']

        except CloudError as e:
            logging.error(e)









