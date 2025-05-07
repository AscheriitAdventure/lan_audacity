from .worker import Worker
from .switch_functions import SwitchFunctions
from qtpy.QtCore import *
from typing import *
import time
from src.models import *
import os
import logging
import inspect
import datetime

BANK_WORDS: list = [
    "Server", "srv", "iLO", "Router", "hub", "Squid", "Switch", "Telnet"
]

class NetworkScanWorker(Worker):
    """
    Worker spécialisé pour effectuer des scans réseau.
    """

    def __init__(self, obj_data: Network, request_d: dict, parent=None):
        super().__init__(obj_data, parent)
        self.objData: Network
        self.request_d: dict = request_d

    def work(self) -> list:
        """
        Effectue le travail réel de scan réseau.
        """
        results = list()
        scan_type = self.request_d.get("type", "nmap")

        if scan_type == "nmap":
            logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {self.objData.web_address.cidr}")
            nb_host = SwitchFunctions.speedScan(SwitchFunctions(), self.objData.web_address.cidr)
            uc_ls = self.objData.get_devices()
            
            logging.info(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Scan Nmap terminé avec {len(nb_host)} hôtes trouvés.")

            for i, host in enumerate(nb_host):
                # Si l'hôte existe déjà dans "devices", on le met à jour
                if any(device.web_address.ipv4 == host for device in uc_ls):
                    logging.info(
                        f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Hôte {host} déjà présent dans devices.")
                    continue
                # Si l'hôte n'existe pas, on le crée
                else:
                    logging.info(
                        f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Hôte {host} ajouté à devices.")
                    var_dir = os.path.join(os.path.dirname(os.path.dirname(self.objData.path)), "desktop")
                    
                    new_device = Device(ospath=var_dir)
                    new_device.web_address.ipv4 = host
                    new_device.web_address.mask_ipv4 = self.objData.web_address.mask_ipv4
                    new_device.web_address.generate_cidr()
                    new_device.update_device()

                    self.objData.devices.append(new_device.get_interface())
                
                self.objData.update_network()

                progress = int((i + 1) / len(nb_host) * 100)
                self.signals.progress.emit(progress)
            
            return nb_host
        
        elif scan_type == "icmp":
            var_tmp = SwitchFunctions.icmpScan(self.request_d.get("ip_addr"))
            logging.info(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Scan ICMP terminé avec {len(var_tmp)} hôtes trouvés.")
            
            return var_tmp
        
        elif scan_type == "snmp":
            pass
        
        # Multi threading imposé
        elif scan_type == "exploration":
            uc_ls = self.objData.get_devices()
            for uc in uc_ls:
                scan: list = SwitchFunctions.fullPortScan(uc)
                filename = "exploration_fps_"+ datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".json"
                d_path1 = os.path.join(os.path.dirname(os.path.dirname(self.objData.path)), "tmp", filename)
                # Save the scan results to a file                
                SwitchFile.json_write(d_path1, scan)
                results.append(d_path1)

                scan.clear()
                
                scan: list = SwitchFunctions.fullOsScan(uc)
                filename = "exploration_fos_"+ datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".json"
                d_path2 = os.path.join(os.path.dirname(os.path.dirname(self.objData.path)), "tmp", filename)
                # Save the scan results to a file
                SwitchFile.json_write(d_path2, scan)
                results.append(d_path2)

                scan.clear()

        # Filtre les résultats en fonction de la banque de mots
        elif scan_type == "osi<5":
            pass
                
        return results

