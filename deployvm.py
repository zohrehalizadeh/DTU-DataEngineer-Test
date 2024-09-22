from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient

# Azure credentials
credential = DefaultAzureCredential()

# Define variables
subscription_id = 'aee8556f-d2fd-4efd-a6bd-f341a90fa76e'
resource_group_name = 'Data_Engineer'  # Resource Group Name
location = 'westeurope'  # Specify your location
vnet_name = 'VNet-ZohrehAlizadeh'
subnet_name = 'Subnet-ZohrehAlizadeh'
nic_name = 'NIC-ZohrehAlizadeh'
vm_name = 'VM-ZohrehAlizadeh'
public_ip_name = 'PublicIP-ZohrehAlizadeh'


# Initialize clients
resource_client = ResourceManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)
compute_client = ComputeManagementClient(credential, subscription_id)

# 1. Create a Virtual Network (VNet)
def create_vnet():
    vnet_params = {
        'location': location,
        'address_space': {
            'address_prefixes': ['10.0.0.0/16']
        }
    }
    vnet_creation = network_client.virtual_networks.begin_create_or_update(
        resource_group_name,
        vnet_name,
        vnet_params
    )
    return vnet_creation.result()

# 2. Create a Network Security Group (NSG)
def create_nsg():
    nsg_params = {
        'location': location,
        'security_rules': [
            {
                'name': 'Allow-SSH',
                'properties': {
                    'protocol': '*',
                    'SourcePortRange': '*',
                    'DestinationPortRange': '22',
                    'SourceAddressPrefix': '*',
                    'DestinationAddressPrefix': '*',
                    'access': 'Allow',
                    'priority': 1000,
                    'direction': 'Inbound'
                }
            }
        ]
    }
    nsg_creation = network_client.network_security_groups.begin_create_or_update(
        resource_group_name,
        f'NSG-{vm_name}',
        nsg_params
    )
    return nsg_creation.result()

# 3. Create a Subnet with NSG association
def create_subnet(nsg):
    subnet_params = {
        'address_prefix': '10.0.0.0/24',
        'network_security_group': {
            'id': nsg.id
        }
    }
    subnet_creation = network_client.subnets.begin_create_or_update(
        resource_group_name,
        vnet_name,
        subnet_name,
        subnet_params
    )
    return subnet_creation.result()

# 4. Create a Public IP Address
def create_public_ip():
    public_ip_params = {
        'location': location,
        'public_ip_allocation_method': 'Static',  # Public static IP
        'sku': {
            'name': 'Standard'  # Use Standard SKU for static IP
        }
    }
    public_ip_creation = network_client.public_ip_addresses.begin_create_or_update(
        resource_group_name,
        public_ip_name,
        public_ip_params
    )
    return public_ip_creation.result()

# 5. Create a Network Interface (NIC)
def create_nic(subnet, public_ip):
    nic_params = {
        'location': location,
        'ip_configurations': [{
            'name': 'IPConfig1',
            'subnet': {'id': subnet.id},
            'private_ip_allocation_method': 'Dynamic',
            'public_ip_address': {'id': public_ip.id}  # Associate the public IP
        }]
    }
    nic_creation = network_client.network_interfaces.begin_create_or_update(
        resource_group_name,
        nic_name,
        nic_params
    )
    return nic_creation.result()

# 6. Deploy the VM
def deploy_vm(nic):
    vm_parameters = {
        "location": location,
        "hardware_profile": {
            "vm_size": "Standard_DS1_v2"
        },
        "storage_profile": {
            "image_reference": {
                "publisher": "Canonical",
                "offer": "0001-com-ubuntu-server-jammy",
                "sku": "22_04-lts-gen2",  # Ubuntu 22.04 LTS
                "version": "latest"
            },
            "os_disk": {
                "create_option": "FromImage"
            }
        },
        "os_profile": {
            "computer_name": vm_name,
            "admin_username": "azureuser",
            "admin_password": "YourPassword123!"  # Replace with a strong password
        },
        "network_profile": {
            "network_interfaces": [
                {
                    "id": nic.id,
                    "primary": True
                }
            ]
        }
    }
    vm_creation = compute_client.virtual_machines.begin_create_or_update(
        resource_group_name,
        vm_name,
        vm_parameters
    )
    return vm_creation.result()

# 7. Set Auto-Shutdown for the VM
def set_auto_shutdown():
    shutdown_time = "17:00"  # 5:00 PM in 24-hour format (CET)
    time_zone = "W. Europe Standard Time"  # CET timezone

    auto_shutdown_settings = {
        "location": location,
        "tags": {"AutoShutdown": "True"},
        "properties": {
            "status": "Enabled",
            "taskType": "ComputeVmShutdownTask",
            "dailyRecurrence": {
                "time": shutdown_time
            },
            "timeZoneId": time_zone,
            "targetResourceId": f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Compute/virtualMachines/{vm_name}"
        }
    }

    return devtestlabs_client.schedules.begin_create_or_update(
        resource_group_name,
        lab_name,
        "shutdown-computevm-" + vm_name,
        auto_shutdown_settings
    ).result()

# Execute the steps
vnet = create_vnet()
print(f"Virtual Network {vnet.name} created.")

nsg = create_nsg()
print(f"Network Security Group {nsg.name} created.")

subnet = create_subnet(nsg)
print(f"Subnet {subnet.name} created.")

public_ip = create_public_ip()
print(f"Public IP {public_ip.name} created.")

nic = create_nic(subnet, public_ip)
print(f"Network Interface {nic.name} created.")

vm = deploy_vm(nic)
print(f"VM {vm.name} created successfully.")

shutdown_schedule = set_auto_shutdown()
print(f"Auto-shutdown configured for 5 PM CET.")