from qtpy.QtWidgets import *
from qtpy.QtCore import *
from src.utils.backend import Worker
from .worker_dialog import WorkerTemplateDialog
from src.models import Network


class NetworkWorkerDialog(WorkerTemplateDialog):
    def __init__(self, network_obj: Network, parent=None, debug=False):
        super().__init__(parent, debug)
        self.network_obj = network_obj
        self.title_window = "Exécution du scan Nmap"
        self.worker = None
        self.thread_pool = QThreadPool()
        self.setupUI()
        
    def setupUI(self):
        # Configurer les éléments d'interface nécessaires
        self.setProgressBar()
        self.setValue(0, 100)
        self.setMessage("Préparation du scan Nmap...")
        self.setTime()
        self.setOperations()
        
        # Ajouter un bouton pour annuler si nécessaire
        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.clicked.connect(self.cancel_scan)
        self.main_layout.addWidget(self.cancel_button)

