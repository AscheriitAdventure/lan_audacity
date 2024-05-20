import sys
import nmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QMovie
import qtawesome as qta

class Signals(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(list)

class Worker(QThread):
    def __init__(self, nmap_function):
        super().__init__()
        self.nmap_function = nmap_function
        self.signals = Signals()

    def run(self):
        try:
            result = self.nmap_function()
            self.signals.result.emit(result)
        except Exception as e:
            self.signals.result.emit([f"Error: {e}"])
        finally:
            self.signals.finished.emit()

class SpinnerBtn(QPushButton):
    def __init__(self, icon=None, parent=None):
        super(SpinnerBtn, self).__init__(parent)
        self.rotateSpinner = False
        self.anmSpinner = qta.Spin(parent_widget=self, autostart=self.rotateSpinner)
        if icon is None:
            self.iconSpinner = qta.icon('fa5s.circle-notch', color='RoyalBlue', animation=self.anmSpinner)
        else:
            self.iconSpinner = icon

        self.setIcon(self.iconSpinner)

    def spin(self):
        self.rotateSpinner = not self.rotateSpinner

        if self.rotateSpinner:
            self.anmSpinner.stop()
        else:
            self.anmSpinner.start()

    def goSpin(self):
        QTimer.singleShot(50, self.spin)

    def stopSpin(self):
        self.anmSpinner.stop()

    def showStatusBtn(self) -> str:
        if self.rotateSpinner:
            return "Threading in progress"
        else:
            return "No threading"



# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle('Exemple PyQt5 avec Icon Spinner')
#         self.setGeometry(100, 100, 400, 200)

#         self.label = QLabel('Cliquez sur le bouton pour lancer Nmap.', self)
#         self.button01 = QPushButton('-sP', self)
#         self.button02 = QPushButton('-sn', self)

#         widget = QWidget()
#         layout = QVBoxLayout(widget)
#         layout.addWidget(self.label)
#         layout.addWidget(self.button01)
#         layout.addWidget(self.button02)
#         self.setCentralWidget(widget)

#         self.button01.clicked.connect(self.start_nmap01)
#         self.button02.clicked.connect(self.start_nmap02)

#         # Ajouter l'icône spinner à la barre de statut
#         self.spinner_label = QPushButton(self)
#         self.spinner_animation = qtawesome.Spin(self.spinner_label, autostart=False)
#         icon = qtawesome.icon('fa5s.circle-notch', color='RoyalBlue', animation=self.spinner_animation)
#         self.spinner_label.setIcon(icon)
#         self.statusBar()

#     def displayMessage(self, message):
#         # display 150 char max
#         self.label.setText(str(message)[:150])
#         self.statusBar().hide(self.spinner_label)

#     def start_nmap_worker(self, nmap_function):
#         self.statusBar().addWidget(self.spinner_label)
#         self.thread = Worker(nmap_function)
#         self.thread.signals.result.connect(self.displayMessage)
#         self.thread.finished.connect(self.stop_spinner)
#         self.thread.finished.connect(self.thread.deleteLater)
#         self.thread.start()

#         # Démarrer l'animation de l'icône spinner
#         self.start_spinner()

#     def start_spinner(self):
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.rotate_spinner)
#         self.angle = 0
#         self.timer.start(50)  # Déclencher toutes les 50 ms

#     def rotate_spinner(self, rotate=True):
#         if rotate:
#             self.spinner_animation.start()
#         else:
#             self.spinner_animation.stop()

#     def stop_spinner(self):
#         self.timer.stop()
#         self.rotate_spinner(False)  # Effacer l'icône spinner lorsque le travail est terminé

#     def nmap01(self):
#         nm = nmap.PortScanner()
#         nm.scan('192.168.90.0/24', arguments='-sP')
#         ls_obj = nm.all_hosts()
#         return ls_obj

#     def nmap02(self):
#         nm = nmap.PortScanner()
#         nm.scan('192.168.90.0/24', arguments='-sn')
#         ls_obj = nm.all_hosts()
#         return ls_obj

#     def start_nmap01(self):
#         self.start_nmap_worker(self.nmap01)

#     def start_nmap02(self):
#         self.start_nmap_worker(self.nmap02)

# def main():
#     app = QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec_())

# if __name__ == '__main__':
#     main()
