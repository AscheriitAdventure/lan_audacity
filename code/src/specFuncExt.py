import logging
import os
import json

from src.classes.cl_network import Network
from src.classes.cl_device import Device
from src.classes.clockManager import ClockManager
from src.classes.switchFile import SwitchFile

def networkDevicesList(net_class:Network) -> list[Device]:
    netClass = net_class
    device_netClass = []
    if netClass.devicesList is not []:
        logging.warning(f"{netClass.name} has {len(netClass.devicesList)} devices saved")
        for uc_unit in netClass.devicesList:
            var_path = os.path.join(
                    os.path.dirname(os.path.dirname(netClass.absPath)),
                    "desktop", f"{uc_unit}.json")
            
            if os.path.exists(var_path):
                logging.debug(f"Loading device {uc_unit} from {var_path}")

                device_data = SwitchFile.json_read(var_path)
                        
                if device_data.get('abs_path') != var_path:
                    true_path = var_path
                else:
                    true_path = device_data.get('abs_path')

                uc_device = Device(
                    device_ipv4=device_data.get('ipv4'),
                    mask_ipv4=device_data.get('mask_ipv4'),
                    save_path=true_path,
                    device_name=device_data.get('name'),
                    uuid_str=device_data.get('uuid')
                )

                clockData = device_data.get('clock_manager')
                uc_device.clockManager = ClockManager(clockData.get('clock_created'), clockData.get('clock_list'))
                if device_data.get('ipv6'):
                    uc_device.ipv6 = device_data.get('ipv6')
                if device_data.get('mac'):
                    uc_device.macAddress = device_data.get('mac')
                if device_data.get('vendor') != "Unknown":
                    uc_device.vendor = device_data.get('vendor')
                
                uc_device.update_auto()
                device_netClass.append(uc_device)

            else:
                logging.warning(f"Device {uc_unit} not found")

        return device_netClass   
    
    else:
        logging.warning(f"{netClass.name} has no devices saved")
        return []
            
def networkList(file_path: str) -> list[Network]:
    netList = []
    if os.path.exists(file_path):
        net_data = SwitchFile.json_read(file_path)

        interfaces_linkList = net_data["networks"]["obj_ls"]
        if len(interfaces_linkList) == 0:
            logging.info("No network found")
            return netList
        else:
            logging.info(f"{len(interfaces_linkList)} network(s) found")
            for interface in interfaces_linkList:
                if os.path.exists(interface.get("path")):
                    net_data = SwitchFile.json_read(interface.get("path"))

                    net_objClass = Network(
                        network_ipv4=net_data['ipv4'], 
                        network_mask_ipv4=net_data['mask_ipv4'], 
                        save_path=net_data['abs_path'],
                        network_name=net_data['name'], 
                        network_ipv6=net_data['ipv6'], 
                        network_gateway=net_data['gateway'],
                        network_dns=net_data['dns'], 
                        uuid_str=net_data['uuid']
                    )
                    net_objClass.clockManager = ClockManager(net_data['clock_manager']['clock_created'], net_data['clock_manager']['clock_list'])
                    if net_data.get('devices'):
                        net_objClass.devicesList = net_data['devices']
                    
                    netList.append(net_objClass)
            
            return netList                    
    else:
        logging.error(f"File {file_path} not found")
        return netList
            