import nmap
import os
from qtpy.QtCore import QObject, Signal, QRunnable, QThread
from qtpy.QtWidgets import QDialog, QProgressBar, QLabel, QVBoxLayout
from typing import Any
import logging

from src.classes.cl_network import Network
from src.classes.cl_device import Device
from src.functionsExt import ip_to_cidr
from src.specFuncExt import networkDevicesList


def scan_listDevices(ipv4: str, mask: str):
    cidr = ip_to_cidr(ipv4, mask)
    nm = nmap.PortScanner()
    nm.scan(hosts=cidr, arguments='-sn')
    return nm.all_hosts()


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
        super(Worker, self).__init__()
        self.objData = obj_data  # Stockage des données nécessaires pour l'opération de travail
        self.exitData = []  # Liste pour stocker les résultats de l'opération
        # Indicateur pour savoir si le travailleur est en cours d'exécution
        self.is_running = True
        self.is_paused = False  # Indicateur pour savoir si le travailleur est en pause
        # Création d'une instance de WorkerSignals pour gérer les signaux
        self.signals = WorkerSignals()

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
        """
        result = []

        # Simulation d'un scan avec une boucle
        for i in range(100):
            if not self.is_running:
                break

            while self.is_paused:
                # Met en pause le thread pendant une courte durée
                QThread.msleep(100)

            # Simulation de l'ajout de données
            result.append(f"Device {i}")

            # Emet un signal de progression (par exemple, un pourcentage ou un nombre d'étapes)
            self.signals.progress.emit(i)

        return result

    def pause(self):
        """
        Met le worker en pause.
        """
        self.is_paused = True

    def resume(self):
        """
        Reprend le worker après une pause.
        """
        self.is_paused = False

    def stop(self):
        """
        Arrête l'exécution du worker.
        """
        self.is_running = False  # Modifie l'indicateur is_running pour indiquer l'arrêt
        self.is_paused = False  # Annule également l'état de pause au cas où


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
        return scan_listDevices(self.objData["ipv4"], self.objData["mask"])


class WDialogs(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading...")
        self.setLayout(QVBoxLayout())
        self.progress_bar = QProgressBar(self)
        self.progress_label = QLabel("Synchronisation en cours...", self)

        self.layout().addWidget(self.progress_label)
        self.layout().addWidget(self.progress_bar)
        self.progress_bar.setValue(0)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def set_message(self, message: str):
        self.progress_label.setText(message)

    def set_maximum(self, max_value: int):
        self.progress_bar.setMaximum(max_value)


class WorkerGetUcList(Worker):
    """
    Worker spécialisé pour récupérer la liste des UC de manière asynchrone.
    """

    def __init__(self, obj_data: Any, parent=None):
        super(WorkerGetUcList, self).__init__(obj_data, parent)

    def work(self) -> list:
        """
        Effectue le travail de récupération de la liste des UC.
        :return: Liste des UC trouvés.
        """
        # Appelle la méthode de récupération des UC avec les paramètres appropriés
        data = self.getUcListAsync()
        logging.debug(f"180: {data}")
        return data

    def getUcListAsync(self) -> list:
        """
        Appelle la méthode `getUcList` de manière asynchrone pour éviter de geler l'interface.
        :return: Liste des UC en format dictionnaire.
        """
        logging.debug(f"188: {self.objData}")
        # self.objData contient ici les données de l'objet Manager
        uc_objClassList = networkDevicesList(self.objData)
        uc_objDict = []

        if uc_objClassList:
            for uc_obj in uc_objClassList:
                # logging.debug(f"Before dict_return: {uc_obj}")
                uc_data = uc_obj.dict_return()
                # logging.debug(f"After dict_return 1: {uc_data}")
                uc_data["status"] = uc_obj.isConnected.name
                # logging.debug(f"After add status: {uc_data}")
                uc_objDict.append(uc_data)

        return uc_objDict


class SyncWorker(Worker):
    def __init__(self, obj_data: Network, parent=None):
        """
        Initialise le worker de périphériques réseau avec des données réseau spécifiques.

        :param obj_data: Données spécifiques à l'objet Network nécessaires pour le travail.
        :param parent: L'objet parent Qt (facultatif).
        """
        # Appelle le constructeur de la classe de base (Worker) avec les paramètres appropriés
        super(SyncWorker, self).__init__(obj_data, parent)

    def work(self) -> None:
        """
        Effectue le travail réel, ici un scan de périphériques.
        """
        lan = ip_to_cidr(self.objData.ipv4, self.objData.maskIpv4)
        path_device = os.path.join(
            os.path.dirname(
                os.path.dirname(self.objData.absPath)),
            "desktop")

        nm = nmap.PortScanner()
        nm.scan(hosts=lan, arguments='-sn')
        logging.debug(f"abspath: {path_device}, list_host: {nm.all_hosts()}, lan: {lan}")

        total_hosts = len(nm.all_hosts())
        for index, host in enumerate(nm.all_hosts()):
            logging.debug("SyncWorker for %s", lan)
            new_device = Device(host, self.objData.maskIpv4, path_device)
            new_device.update_auto()
            new_device.save_file()

            # Ajout de l'appareil au réseau
            self.objData.add_device(new_device)
            self.objData.save_network()

            # Mise à jour de la progression
            progress = int((index + 1) / total_hosts * 100)
            self.signals.progress.emit(progress)
