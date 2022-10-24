from dataclasses import field, fields
from operator import contains
from pprint import pprint
from netmiko import ConnectHandler

cisco_device = {
    'device_type': 'cisco_ios',
    'host': '10.10.40.46',
    'username': 'netmiko',
    'password': 'netmiko-password',
    'secret': 'enable-secret',
}

vlan_to_search = input("Enter VLAN to search for:")

# Make this into a function with variable: enable command
ssh = ConnectHandler(**cisco_device)
ssh.enable()
output = ssh.send_command('show vlan')
ssh.disconnect

def pull_vlans(show_vlan_output):
    vlan_list = {}
    
    for line in show_vlan_output.splitlines():
        if "VLAN" in line or "-----" in line:
            continue
        
        fields = line.split()
        # remove empty lists
        if len(fields) == 0:
            continue
        # identify vlan id and vlan name
        vlan_id = fields[0]
        vlan_name = fields[1]
        if vlan_id == "1002":
            break
        # add vlan number and name to list
        vlan_list.append((vlan_id, vlan_name))
        #print(vlan_list)
    return(vlan_list)

pull_vlans(output)

def search_for_vlan(vlan):
    for item in pull_vlans(output):
        if item[0] == vlan:
            print(item)


search_for_vlan(vlan_to_search)
