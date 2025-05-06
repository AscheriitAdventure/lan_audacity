from .worker_signals import WorkerSignals
from qtpy.QtCore import QRunnable, QThread
from typing import Any


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

