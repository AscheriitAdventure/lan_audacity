"""
    C'est un fichier de test qui a pour but d'ouvrir deux fenêtres PyQt6.
    Avec ces deux fenêtres (wind1 et wind2), on peut les manipuler.
    Sur wind1, on va afficher un bouton qui va lancer une action sur wind2.
    Et quand wind2 aura fini son action, il va envoyer un signal à wind1 pour lui dire que c'est fini.
    wind1 va alors afficher un message pour dire que c'est fini.
"""

import sys
from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QProgressBar,
)
from qtpy.QtCore import Signal, QObject, QTimer


# Définir un objet pour créer le signal personnalisé
class Communication(QObject):
    finished = Signal()


# Fenêtre 1 (wind1)
class Window1(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Window 1")
        self.setGeometry(100, 100, 300, 200)

        # Création du bouton
        self.button = QPushButton("Start Action in Window 2", self)
        self.button.clicked.connect(self.start_action_in_window2)

        # Label pour afficher le message de fin d'action
        self.message_label = QLabel("", self)

        # Barre de progression (initialement cachée)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.message_label)
        layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Instancier la fenêtre 2
        self.window2 = Window2()

        # Connecter le signal "finished" de window2 à la méthode qui affiche le message
        self.window2.comm.finished.connect(self.on_action_finished)

        # Connecter le signal de résultat
        self.window2.result_signal.connect(self.receive_result)

        # Stocker le résultat à afficher
        self.result = None

    def start_action_in_window2(self):
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(50)
        # self.window2.show()
        self.window2.start_action()

    def on_action_finished(self):
        """Méthode appelée lorsque l'action de Window2 est terminée."""
        self.progress_bar.setValue(100)
        self.progress_bar.setVisible(False)

    def receive_result(self, result):
        """Méthode appelée lorsque Window2 envoie le résultat."""
        # Mettre à jour le label directement avec le résultat
        self.result = result
        self.message_label.setText(f"Résultat reçu : {self.result}")


# Fenêtre 2 (wind2)
class Window2(QMainWindow):
    result_signal = Signal(str)  # Signal défini correctement

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Window 2")
        self.setGeometry(450, 100, 300, 200)

        # Créer un objet de communication pour le signal personnalisé
        self.comm = Communication()

        # Un label pour montrer l'état de l'action dans cette fenêtre
        self.action_label = QLabel("Action not started", self)
        layout = QVBoxLayout()
        layout.addWidget(self.action_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_action(self):
        # Simuler une action (par exemple changer le texte après un certain temps)
        self.action_label.setText("Action in progress...")

        # Simuler la fin de l'action après une courte période
        QTimer.singleShot(6000, self.end_action)

    def end_action(self):
        # Mettre à jour l'UI de cette fenêtre
        self.action_label.setText("Action finished")

        # Calculer ou effectuer l'opération et obtenir le résultat
        result = "Résultat de l'opération"  # Remplacez cela par votre propre calcul ou opération

        # Emettre le signal avec le résultat
        self.result_signal.emit(result)

        # Emettre un signal indiquant que l'action est terminée
        self.comm.finished.emit()

        # Fermer cette fenêtre (Window 2)
        self.close()


# Code principal pour lancer l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Créer et afficher la fenêtre 1
    window1 = Window1()
    window1.show()

    sys.exit(app.exec())
