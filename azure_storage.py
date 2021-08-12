
import client_handlers
import azure_storage_base
import threading,time
import logging
from msrestazure.azure_exceptions import CloudError
logging.getLogger().setLevel(logging.INFO)


class BuildStorage(azure_storage_base.BaseStorage):

    def __init__(self,subscription_id,storageName):
        super(BuildStorage, self).__init__(subscription_id)
        self.storageName = storageName

    def create_sas(self):
        try:
            logging.info('create read sas')
            key = self.find_key(self.storageName)
            time.sleep(2)
            if key:
                return client_handlers.ClientHandlers.create_account_sas(self.storageName,key)
            else:
                return client_handlers.ClientHandlers.static_reply()[0]

        except CloudError as e:
            logging.error(e)

    def create_admin_sas(self):
        try:
            print('create admin sas')
            key = self.find_key(self.storageName)
            time.sleep(2)
            if key:
                return client_handlers.ClientHandlers.create_account_admin_sas(self.storageName,key)
            else:
                return client_handlers.ClientHandlers.static_reply()[0]

        except CloudError as e:
            logging.error(e)

    def fetching_sas(self):
        try:
            if self.find_rg_of_storage(storageName=self.storageName):
                try:
                    logging.info('trying to get keys from table, searching in Table........')
                    key = client_handlers.ClientHandlers.get_entry_from_table(storageName=self.storageName,subscription_id=self.subscription_id)
                    if key:
                        logging.info("key found in Table storage")
                        return key
                except Exception as e:
                    logging.error(e)
                    logging.info("key does not found !!!  creating new entry......")
                    storage_detail = {'PartitionKey': self.subscription_id, 'RowKey': self.storageName, 'rs': self.create_sas(), 'ws':self.create_admin_sas()}
                    new_entry=client_handlers.ClientHandlers.entry_to_table(storage_detail)
                    if new_entry:
                        logging.info('successfully created new entry in table')
                        return client_handlers.ClientHandlers.get_entry_from_table(storageName=self.storageName,subscription_id=self.subscription_id)
            else:
                return client_handlers.ClientHandlers.static_reply()[0]

        except CloudError as e:
            logging.error(e)
