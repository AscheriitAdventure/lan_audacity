import sys
from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout
from qtpy.QtWebEngineWidgets import QWebEngineView
from qtpy.QtCore import QUrl
from pyvis.network import Network
from pathlib import Path


class NetworkVisualization(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Network Visualization')
        self.setGeometry(100, 100, 800, 600)

        # Créer une instance de Network
        net = Network()

        # Ajouter des nœuds
        net.add_node(1, label="Routeur", shape='image', image="C:\\Users\\g.tronche\\Documents\\GitHub\\lan_audacity\\code\\assets\\svg\\router.svg")
        net.add_node(2, label="Wireless Router", shape='image', image="C:\\Users\\g.tronche\\Documents\\GitHub\\lan_audacity\\code\\assets\\svg\\wireless-router.svg")
        net.add_node(3, label="Switch L2", shape='image', image="C:\\Users\\g.tronche\\Documents\\GitHub\\lan_audacity\\code\\assets\\svg\\layer-2-switch.svg")

        # Ajouter des arêtes
        net.add_edge(1, 2)
        net.add_edge(1, 3)
        net.add_edge(2, 3)

        # Générer le fichier HTML
        net.show("index.html", notebook=False)

        # Créer un QWebEngineView pour afficher le fichier HTML
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl.fromLocalFile(str(Path("index.html").resolve())))

        # Créer un layout et ajouter le QWebEngineView
        layout = QVBoxLayout()
        layout.addWidget(self.web_view)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NetworkVisualization()
    ex.show()
    sys.exit(app.exec_())
