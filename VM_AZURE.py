""" 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED 
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Microsoft Create VM on Azure Python 3 
Yrwins Acosta
yrwins@gmail.com
May 2020, version 1.2
"""

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute.models import DiskCreateOption

# This part if for AZURE Subcription and Subscription ID. 
#you can edit this part  
SUBSCRIPTION_ID = 'copy_you_AZURE_Subscripton_ID'
GROUP_NAME = 'Name_of_Group'
LOCATION = 'Copy_You_LOCATION'
VM_NAME = 'Name_of_VM'
VNET = 'Name_of_Vnet'
VNET_SUBNET = 'Name_of_Subnet'

def get_credentials():
    credentials = ServicePrincipalCredentials(
        client_id = 'Copy_You_AZURE_Application_client_ID',
        secret = 'Copy_You_Certificate_Client_secrets',
        tenant = 'Copy_You_AZURE_Tenant_ID'
    )

    return credentials

def create_resource_group(resource_group_client):
    resource_group_params = { 'location':LOCATION }
    resource_group_result = resource_group_client.resource_groups.create_or_update(
        GROUP_NAME,
        resource_group_params
    )

#This part if for AZURE Computer Client.
def create_availability_set(compute_client):
    avset_params = {
        'location': LOCATION,
        'sku': { 'name': 'Aligned' },
        'platform_fault_domain_count': 3
    }
    availability_set_result = compute_client.availability_sets.create_or_update(
        GROUP_NAME,
        'myAVSet',
        avset_params
    )

#This part if for AZURE Network setup, 
#You can edit the type of Public ip. 
def create_public_ip_address(network_client):
    public_ip_addess_params = {
        'location': LOCATION,
        'public_ip_allocation_method': 'Dynamic'
    }
    creation_result = network_client.public_ip_addresses.create_or_update(
        GROUP_NAME,
        'myIPAddress',
        public_ip_addess_params
    )

    return creation_result.result()

#this part if for AZURE Vnet setup. 
#you can edit the ip address 
def create_vnet(network_client):
    vnet_params = {
        'location': LOCATION,
        'address_space': {
            'address_prefixes': ['10.0.0.0/16']
        }
    }
    creation_result = network_client.virtual_networks.create_or_update(
        GROUP_NAME,
        VNET,
        vnet_params
    )
    return creation_result.result()

#This part if for AZURE VM Subnet ip address setup
#you can edit the ip address 
def create_subnet(network_client):
    subnet_params = {
        'address_prefix': '10.0.0.0/24'
    }
    creation_result = network_client.subnets.create_or_update(
        GROUP_NAME,
        VNET,
        VNET_SUBNET,
        subnet_params
    )

    return creation_result.result()

#This part if for AZURE Network Card
def create_nic(network_client):
    subnet_info = network_client.subnets.get(
        GROUP_NAME,
        VNET,
        VNET_SUBNET
    )
    publicIPAddress = network_client.public_ip_addresses.get(
        GROUP_NAME,
        'myIPAddress'
    )
    nic_params = {
        'location': LOCATION,
        'ip_configurations': [{
            'name': 'myIPConfig',
            'public_ip_address': publicIPAddress,
            'subnet': {
                'id': subnet_info.id
            }
        }]
    }
    creation_result = network_client.network_interfaces.create_or_update(
        GROUP_NAME,
        'myNic',
        nic_params
    )

    return creation_result.result()

def create_vm(network_client, compute_client):
    nic = network_client.network_interfaces.get(
        GROUP_NAME,
        'myNic'
    )
    avset = compute_client.availability_sets.get(
        GROUP_NAME,
        'myAVSet'
    )
    #you can edit username and password
    vm_parameters = {
        'location': LOCATION,
        'os_profile': {
            'computer_name': VM_NAME,
            'admin_username': 'yourusername',
            'admin_password': 'Yourpassword01!'
        },
        #you can edit the type of vm 
        'hardware_profile': {
            'vm_size': 'Standard_DS1'
        },
        #you can edit the type of image
        'storage_profile': {
            'image_reference': {
                'publisher': 'Canonical',
                'offer': 'win2016datacenter',
                'sku': 'B1ls',
                'version': 'latest'
            }
        },
        'network_profile': {
            'network_interfaces': [{
                'id': nic.id
            }]
        },
        'availability_set': {
            'id': avset.id
        }
    }
    creation_result = compute_client.virtual_machines.create_or_update(
        GROUP_NAME,
        VM_NAME,
        vm_parameters
    )

    return creation_result.result()

def start_vm(compute_client):
    compute_client.virtual_machines.start(GROUP_NAME, VM_NAME)

if __name__ == "__main__":

    credentials = get_credentials()

    resource_group_client = ResourceManagementClient(
        credentials,
        SUBSCRIPTION_ID
    )
    network_client = NetworkManagementClient(
        credentials,
        SUBSCRIPTION_ID
    )
    compute_client = ComputeManagementClient(
        credentials,
        SUBSCRIPTION_ID
    )

create_resource_group(resource_group_client)
print("\n 12.5% Done, Please Wait for AZURE \nthat is Creating Resource Group")

create_availability_set(compute_client)
print("\n25% Done, Please Wait for AZURE \nthat is Creating Availability Set")

creation_result = create_public_ip_address(network_client)
print("\n37.5% Done, Please Wait for AZURE \nthat is Creating Public IP")

creation_result = create_vnet(network_client)
print("\n50% Done, Please Wait for AZURE \nthat is Creating VNET")

creation_result = create_subnet(network_client)
print("\n62.5% Done, Please Wait for AZURE \nthat is Creating Subnet")

creation_result = create_nic(network_client)
print("\n75% Done, Please Wait for AZURE \nthat is Creating NIC")

creation_result = create_vm(network_client, compute_client)
print("\n\n 12.5% Done, Please Wait for AZURE \nthat is Creating Virtual Machine")

start_vm(compute_client)
print("\n100% Done, Please Wait for AZURE \nthat is Complete! Starting Virtual Machine")
