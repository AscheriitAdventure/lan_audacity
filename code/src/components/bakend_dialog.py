import nmap
from qtpy.QtCore import QObject, Signal, QRunnable
from qtpy.QtWidgets import QDialog, QProgressBar, QLabel, QVBoxLayout
from typing import Any
import subprocess
import platform

from src.classes.cl_network import Network
from src.functionsExt import ip_to_cidr


def scan_listDevices(ipv4:str, mask:str):
    cidr = ip_to_cidr(ipv4, mask)
    nm = nmap.PortScanner()
    nm.scan(hosts=cidr, arguments='-sn')
    return nm.all_hosts()

def scan_deviceAllPorts(ip:str):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip, arguments='-p 1-65535 -T4 -A')
    return nm[ip]

def scan_deviceSpecificPorts(ip:str, ports:str):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip, arguments=f'-p {ports} -T4 -A -v')
    return nm[ip]

def scan_deviceOs(ip:str):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip, arguments='-O')
    return nm[ip]

def scan_pingDevice(ip: str) -> bool:
    """
    Vérifie si un périphérique répond à un ping à l'aide de subprocess.
    
    :param ip: L'adresse IP du périphérique à scanner.
    :return: True si l'adresse IP répond, sinon False.
    """
    # Détermine la commande de ping selon le système d'exploitation (Windows ou autre)
    param = "-n" if platform.system().lower() == "windows" else "-c"
    
    # Prépare la commande de ping
    command = ["ping", param, "1", ip]
    
    try:
        # Exécute la commande de ping et vérifie la sortie
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Vérifie si le périphérique répond au ping en cherchant un code de retour 0
        if output.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        # Gestion des exceptions, par exemple en cas d'erreur de sous-processus
        print(f"Erreur lors du ping de {ip}: {e}")
        return False


class WorkerSignals(QObject):
    """
    Classe qui définit des signaux utilisés pour communiquer avec d'autres objets Qt.
    """
    # Signal émis lorsque le travail commence
    started = Signal()

    # Signal émis lorsque le travail est terminé
    finished = Signal()

    # Signal émis pour indiquer la progression du travail (avec un entier représentant le pourcentage ou l'étape)
    progress = Signal(int)

    # Signal émis pour retourner les résultats du travail sous forme de liste
    result = Signal(list)


class Worker(QRunnable):
    """
    Classe représentant un worker (travailleur) qui effectue des opérations de manière asynchrone.
    """
    def __init__(self, obj_data: Any, parent=None):
        """
        Initialise le worker avec des données et prépare les attributs nécessaires.

        :param obj_data: Données nécessaires pour effectuer le travail, sous forme d'un objet ou d'un dictionnaire.
        :param parent: L'objet parent Qt (facultatif).
        """
        super(Worker, self).__init__(parent)
        self.objData = obj_data  # Stockage des données nécessaires pour l'opération de travail
        self.exitData = []  # Liste pour stocker les résultats de l'opération
        self.is_running = True  # Indicateur pour savoir si le travailleur est en cours d'exécution
        self.signals = WorkerSignals()  # Création d'une instance de WorkerSignals pour gérer les signaux

    def run(self):
        """
        Méthode principale du worker, appelée pour démarrer le travail asynchrone.
        """
        # Emet le signal de début de travail
        self.signals.started.emit()

        # Exécute la méthode de travail et stocke les résultats dans exitData
        self.exitData = self.work()

        # Emet le signal pour transmettre les résultats obtenus
        self.signals.result.emit(self.exitData)

        # Emet le signal de fin de travail
        self.signals.finished.emit()

    def work(self) -> list:
        """
        Effectue le travail réel, ici un scan de périphériques.

        :return: Liste des résultats du scan.
        """
        # Appelle la fonction de scan avec les paramètres appropriés provenant de objData
        return scan_listDevices(self.objData["ipv4"], self.objData["mask"])

    def stop(self):
        """
        Arrête l'exécution du worker.
        """
        self.is_running = False  # Modifie l'indicateur is_running pour indiquer l'arrêt


class WorkerDevice(Worker):
    """
    Classe représentant un worker spécialisé pour gérer les périphériques réseau.
    """
    def __init__(self, obj_data: Network, parent=None):
        """
        Initialise le worker de périphériques réseau avec des données réseau spécifiques.

        :param obj_data: Données spécifiques à l'objet Network nécessaires pour le travail.
        :param parent: L'objet parent Qt (facultatif).
        """
        # Appelle le constructeur de la classe de base (Worker) avec les paramètres appropriés
        super(WorkerDevice, self).__init__(obj_data, parent)

    def work(self) -> list:
        """
        Effectue le travail réel, ici un scan de périphériques.
        
        :return: Liste des résultats du scan.
        """
        # Appelle la fonction de scan avec les paramètres appropriés provenant de objData
        return scan_listDevices(self.objData.ipv4, self.objData.maskIpv4)


class WorkersPing(Worker):
    """
    Classe représentant un worker spécialisé pour gérer le ping d'un périphérique réseau.
    """
    def __init__(self, obj_data: list, parent=None):
        """
        Initialise le worker de ping avec des données spécifiques.

        :param obj_data: Données spécifiques nécessaires pour le travail.
        :param parent: L'objet parent Qt (facultatif).
        """
        # Appelle le constructeur de la classe de base (Worker) avec les paramètres appropriés
        super(WorkersPing, self).__init__(obj_data, parent)

    def work(self) -> list:
        """
        Effectue le travail réel, ici un ping d'un périphérique réseau.

        :return: Liste des résultats du ping.
        """
        ip_infos = []
        for index, device in enumerate(self.objData):
            device = {
                "ipv4": device["ipv4"], 
                "is_online": scan_deviceAllPorts(device["ipv4"])
            }
            ip_infos.append(device)

            # Update progress
            progress = int(index + 1) * 100 // len(self.objData)
            self.signals.progress.emit(progress)

        return ip_infos


class WDialogs(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Synchronisation")
        self.setLayout(QVBoxLayout())
        self.progress_bar = QProgressBar(self)
        self.progress_label = QLabel("Synchronisation en cours...", self)

        self.layout().addWidget(self.progress_label)
        self.layout().addWidget(self.progress_bar)
        self.progress_bar.setValue(0)

    def update_progress(self, value):
        self.progress_bar.setValue(value)