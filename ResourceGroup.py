from azure.mgmt.common import SubscriptionCloudCredentials
from azure.mgmt.resource import ResourceManagementClient

class Azure_resourceGroup:
    def __init__(self,credential,subscriptionid):
        self.credential=credential
        self.subscriptionid=subscriptionid
    def creating_client(self):
        return ResourceManagementClient(credentials=self.credential, subscription_id=self.subscriptionid)

    def createResourceGroup(self,resourceGroupName,location):
        parameter={"location":location}
        client=self.creating_client()

        ResourceGroup= client.resource_groups.create_or_update(resourceGroupName,parameter)
        print (ResourceGroup)

    def list_all_resourcegroup(self):
        rg_list = []
        client= self.creating_client()
        list_of_ResourceGroup=client.resource_groups.list()

        for i in list_of_ResourceGroup:

          rg_list.append({"name":i.name,"location":i.location,"tag":i.tags})#
        return rg_list


    def remove_resourcegroup(self, resourceGroupName):
        client= self.creating_client()
        deletion_rg =client.resource_groups.delete(resourceGroupName)
        return deletion_rg

    def find_resourcegroup(self,resourcegroupname,location):
        listofrg= self.list_all_resourcegroup()
        for element in listofrg:
            if element['name']==resourcegroupname and element['location']==location:
                return True
        else:
            return False

    def modify_tag_in_resourceGroup(self,resourcegroupname,location,tag={}):
        if self.find_resourcegroup(resourcegroupname,location) == True:
            parameter={"location":location,"Tags":tag}
            client=self.creating_client()
            updated_rg=client.resource_groups.create_or_update(resource_group_name=resourcegroupname,parameters=parameter)

            print "Tag has been updated to the resource group"

        else:
            print "Resource group is not exist"



