import sys
import asyncio
import nmap
from PyQt6.QtCore import Qt, QThread, pyqtSignal as Signal
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QProgressBar


class Worker(QThread):
    finished = Signal()
    error_occurred = Signal(str)
    progress_changed = Signal(int)

    def __init__(self, async_function, parent=None):
        super().__init__(parent)
        self.async_function = async_function

    def run(self):
        try:
            asyncio.run(self.async_function(self.progress_changed))
            self.finished.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self, async_function, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Analyse de ports avec Nmap")
        self.setGeometry(100, 100, 400, 200)

        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.statusBar().addPermanentWidget(self.progress_bar)

        self.worker = Worker(async_function)
        self.worker.finished.connect(self.on_finished)
        self.worker.error_occurred.connect(self.on_error_occurred)
        self.worker.progress_changed.connect(self.progress_bar.setValue)

        self.show_loading_message()
        self.worker.start()

    def show_loading_message(self):
        QMessageBox.information(self, "Chargement", "Analyse en cours...", QMessageBox.StandardButton.NoButton)

    def on_finished(self):
        self.progress_bar.setValue(100)
        QMessageBox.information(self, "Succès", "Votre fonction a terminé.", QMessageBox.StandardButton.NoButton)
        self.close()

    def on_error_occurred(self, error_message):
        QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite : {error_message}",
                             QMessageBox.StandardButton.Ok)
        self.close()


async def perform_port_scan(progress_callback):
    nm = nmap.PortScannerAsync()
    scan_result = await nm.scan('192.168.1.1/24', arguments='-p 22,80,443', callback=progress_callback)
    print(scan_result)


def main():
    app = QApplication(sys.argv)
    window = MainWindow(perform_port_scan)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
