import adal
import requests

class AzureAuth:

  def __init__(self,application_id,application_secret,tenant_id):

    self.application_id=application_id
    self.application_secret=application_secret
    self.tenant_id =tenant_id
    self.authentication_endpoint = 'https://login.microsoftonline.com/'
    self.resource = 'https://management.core.windows.net/'

  def azureauthentication(self):  #creating the access token #
    context = adal.AuthenticationContext(self.authentication_endpoint + self.tenant_id)
    token_response = context.acquire_token_with_client_credentials(self.resource, self.application_id, self.application_secret)
    access_token =token_response.get("accessToken")


    return access_token
