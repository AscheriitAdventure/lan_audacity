from dataclasses import dataclass
import os
import logging

@dataclass
class OsSys:
    name: str
    version: str

    def exec_os(self) -> bool:
        if self.name in ['Windows', 'Linux', 'Darwin']:
            return True
        else:
            logging.error(f"Operating System '{self.name} {self.version}' not supported.")
            return False
        
    def exec_software(self) -> int:
        # search for nmap, docker, and python
        software_list = ['nmap', 'docker', 'python']
        var_i = 0
        if self.name == 'Windows':
            for software in software_list:
                if os.system(f"where {software} >nul 2>nul") == 0:
                    logging.info(f"{software} is installed.")
                else:
                    logging.warning(f"{software} is not installed.")
                    var_i += 1
        elif self.name in ['Linux', 'Darwin']:
            for software in software_list:
                if os.system(f"which {software} > /dev/null 2>&1") == 0:
                    logging.info(f"{software} is installed.")
                else:
                    logging.warning(f"{software} is not installed.")
                    var_i += 1
        else:
            logging.error(f"Operating System '{self.name}' not supported.")
            var_i += 1
        
        return var_i
