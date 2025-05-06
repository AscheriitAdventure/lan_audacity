from qtpy.QtCore import QObject, Signal

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

