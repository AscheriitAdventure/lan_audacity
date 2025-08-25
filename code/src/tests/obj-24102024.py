import platform
import subprocess
import logging
from src.components.eunum_lab import isConnected


class NetObject:
    def __init__(self):
        self.ipv4 = "192.168.253.100"
        self.isConnected = isConnected.NOT_SETTED

    def set_isConnected(self) -> None:
        # Vérifie l'OS et utilise le bon paramètre pour le ping
        param = "-n" if platform.system().lower() == "windows" else "-c"
        try:
            result = subprocess.run(
                ["ping", param, "4", self.ipv4],  # Utilise le paramètre en fonction de l'OS
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
            )
            if result.returncode == 0:
                self.isConnected = isConnected.CONNECTED
                logging.info("La machine est connectée.")
            else:
                self.isConnected = isConnected.DISCONNECTED
                logging.warning("La machine n'est pas connectée.")
        except subprocess.TimeoutExpired:
            self.isConnected = isConnected.DISCONNECTED
            logging.warning("Timeout lors de la tentative de connexion à la machine.")


if __name__ == "__main__":
    obj = NetObject()
    obj.set_isConnected()
    print(obj.isConnected.name)


# Alphabetique Order : 0-9A-Z
# Alphabetique Order : Z-A9-0
#
