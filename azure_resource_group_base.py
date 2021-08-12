from static_handler_utils import StaticHandlers
import client_handlers
import logging
from msrestazure.azure_exceptions import  CloudError
logging.getLogger().setLevel(logging.INFO)


class BaseRg:

    def __init__(self,subscription_id):
        self.subscription_id = subscription_id

    def list_rg(self):
        try:
            cred_object = StaticHandlers.read_secret()
            credentials = client_handlers.ClientHandlers.login_to_azure(**cred_object)
            rg_list = []
            logging.info("generating rg lists......")
            generator = list(client_handlers.ClientHandlers.get_resource_client(credentials,self.subscription_id).
                             resource_groups.list())
            num_of_files = sum(1 for _ in generator)
            if num_of_files == 0 :
                raise Exception("No rg is present with prefix/name  in subscription")
            else:
                for rgs in generator:
                    rg_list.append(rgs.name)
                return rg_list
        except CloudError as e:
            logging.error(e)



