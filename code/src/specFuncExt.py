import logging, inspect
import os
from typing import List

from src.classes.cl_network import Network
from src.classes.cl_device import Device
from src.classes.clockManager import ClockManager
from src.classes.switchFile import SwitchFile


def networkDevicesList(net_class: Network) -> List[Device]:
    net_list = net_class.devicesList
    devices: List[Device] = []
    if isinstance(net_list, list) and len(net_list) > 0:
        logging.info(f"{inspect.currentframe().f_code.co_name}: {net_class.name} has {len(net_list)} devices saved")
        for uc in net_list:
            var_path = os.path.join(os.path.dirname(os.path.dirname(net_class.absPath)),"desktop", f"{uc}.json")

            tmp_dict: dict = dict()

            if os.path.exists(var_path):
                logging.debug(f"{inspect.currentframe().f_code.co_name}: Loading device {uc} from {var_path}")

                uc_data = SwitchFile.json_read(var_path)
                
                tmp_dict["save_path"] = var_path if uc_data.get('abs_path') != var_path else uc_data.get('abs_path')
                tmp_dict["device_name"] = uc_data.get('name')
                tmp_dict["uuid_str"] = uc_data.get('uuid', None)
                tmp_dict["device_ipv4"] = uc_data.get('ipv4')
                tmp_dict["mask_ipv4"] = uc_data.get('mask_ipv4')

                logging.debug(f"{inspect.currentframe().f_code.co_name}: dict: {tmp_dict}")

                uc__obj = Device(**tmp_dict)
                clock_obj = uc_data.get('clock_manager')
                uc__obj.clockManager = ClockManager(clock_obj.get('clock_created'), clock_obj.get('clock_list'))
                if uc_data.get('ipv6'):
                    uc__obj.ipv6 = uc_data.get('ipv6')
                if uc_data.get('mac'):
                    uc__obj.macAddress = uc_data.get('mac')
                if uc_data.get('vendor') != "Unknown":
                    uc__obj.vendor = uc_data.get('vendor')
                
                uc__obj.update_auto()
                devices.append(uc__obj)
                
            else:
                net_class.devicesList.remove(uc)
                logging.warning(f"Device {uc} not found")
                continue
        
    return devices

def networkList(file_path: str) -> list[Network]:
    netList = []
    if os.path.exists(file_path):
        net_data = SwitchFile.json_read(file_path)

        interfaces_linkList = net_data["networks"]["obj_ls"]
        if len(interfaces_linkList) == 0:
            logging.info("No network found")
            return netList
        else:
            logging.info(f"{inspect.currentframe().f_code.co_name}: {len(interfaces_linkList)} network(s) found")
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
        logging.error(f"{inspect.currentframe().f_code.co_name}: File {file_path} not found")
        return netList
            