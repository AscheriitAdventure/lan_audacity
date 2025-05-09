from qtpy.QtWidgets import *
from qtpy.QtCore import *
from src.utils.backend import NetworkScanWorker
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

    def start_scan(self, scan_data:dict = {"type": "nmap",}):

        # Créer le worker
        self.worker = NetworkScanWorker(self.network_obj, scan_data)

        # Connecter les signaux
        self.worker.signals.started.connect(self.on_started)
        self.worker.signals.progress.connect(self.on_progress)
        self.worker.signals.result.connect(self.on_result)
        self.worker.signals.finished.connect(self.on_finished)

        # Démarrer le worker dans un thread séparé
        self.thread_pool.globalInstance().start(self.worker)

    def cancel_scan(self):
        if self.worker:
            self.worker.stop()
            self.logOperation("Scan annulé par l'utilisateur")

    def on_started(self):
        self.logOperation("Démarrage du scan Nmap")
        # Mettre à jour le statut dans la carte "Status of the Runnable Actions"
        # self.network_obj.update_status("nmap", "In Progress") # ??????

    def on_progress(self, progress):
        self.updateProgress(progress)
        if progress % 10 == 0:  # Log périodique
            self.logOperation(f"Scan en cours ({progress}%)")

    def on_result(self, results):
        # Traiter les résultats
        self.logOperation("Traitement des résultats")
        # Mettre à jour les cartes avec les nouvelles données
        # self.network_obj.update_devices(results)

    def on_finished(self):
        self.completeOperation("Scan Nmap")
        self.logOperation("Scan terminé avec succès")
        # Mettre à jour le statut dans la carte
        # self.network_obj.update_status("nmap", "Completed") # ??????
        # Fermer la boîte de dialogue après un court délai
        QTimer.singleShot(2000, self.accept)
