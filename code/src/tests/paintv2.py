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
        net.show_buttons(filter_=['physics'])
        net.filter_menu = True
        net.select_menu = True
        nodeList = [
            {
                "id": 0,
                "label": "Cloud",
                "shape": "image",
                "image": "C:\\Users\\g.tronche\\Documents\\GitHub\\affinity\\svg\\circle\\blue\\c_cloud_blue.svg", 
                "links": []
            },
            {
                "id": "fldjhgcv",
                "label": "Firewall",
                "shape": "image",
                "image": "C:\\Users\\g.tronche\\Documents\\GitHub\\affinity\\svg\\circle\\blue\\c_firewall_blue.svg",
                "links": [0]
            },
            {
                "id": 2,
                "label": "4G Router",
                "shape": "image",
                "image": "C:\\Users\\g.tronche\\Documents\\GitHub\\affinity\\svg\\square\\blue\\sq_satellite_dish_blue.svg",
                "links": ["fldjhgcv"]
            },
            {
                "id": 3,
                "label": "Load Balancer",
                "shape": "image",
                "image": "C:\\Users\\g.tronche\\Documents\\GitHub\\affinity\\svg\\circle\\blue\\c_loadbalancer_blue.svg",
                "links": ["fldjhgcv"]
            },
            {
                "id": 4,
                "label": "Switch L3\nPrimary",
                "shape": "image",
                "image": "C:\\Users\\g.tronche\\Documents\\GitHub\\affinity\\svg\\circle\\blue\\c_switch_multilayer_blue.svg",
                "links": [3]
            },
            {
                "id": 5,
                "label": "Switch L3\nSecondary",
                "shape": "image",
                "image": "C:\\Users\\g.tronche\\Documents\\GitHub\\affinity\\svg\\circle\\blue\\c_switch_multilayer_blue.svg",
                "links": [3, 4]
            },
            {
                "id": 6,
                "label": "Switch L3\nSpare",
                "shape": "image",
                "image": "C:\\Users\\g.tronche\\Documents\\GitHub\\affinity\\svg\\circle\\blue\\c_switch_multilayer_blue.svg",
                "links": [3, 4, 5]
            },
            {
                "id": 7,
                "label": "Server Cluster\nPrimary",
                "shape": "image",
                "image": "C:\\Users\\g.tronche\\Documents\\GitHub\\affinity\\svg\\circle\\blue\\c_server-cluster_blue.svg",
                "links": [4, 5]
            },
            {
                "id": 8,
                "label": "Server Cluster\nSecondary",
                "shape": "image",
                "image": "C:\\Users\\g.tronche\\Documents\\GitHub\\affinity\\svg\\circle\\blue\\c_server-cluster_blue.svg",
                "links": [4, 5, 7]
            },
            {
                "id": 9,
                "label": "Router Wireless\nMaster",
                "shape": "image",
                "image": "C:\\Users\\g.tronche\\Documents\\GitHub\\affinity\\svg\\circle\\blue\\c_wireless_blue.svg",
                "links": [5]
            },
            {
                "id": 10,
                "label": "Router Wireless\nSlave",
                "shape": "image",
                "image": "C:\\Users\\g.tronche\\Documents\\GitHub\\affinity\\svg\\circle\\blue\\c_wireless_blue.svg",
                "links": [5]
            },
            {
                "id": 11,
                "label": "NAS Server",
                "shape": "image",
                "image": "C:\\Users\\g.tronche\\Documents\\GitHub\\affinity\\svg\\circle\\blue\\c_nas_blue.svg",
                "links": [4, 5]
            },
            {
                "id": 12,
                "label": "Switch L2\nBuilding ZAC",
                "shape": "image",
                "image": "C:\\Users\\g.tronche\\Documents\\GitHub\\affinity\\svg\\circle\\blue\\c_switch_blue.svg",
                "links": [5]
            }
        ]
        # Ajouter des nœuds
        for node in nodeList:
            net.add_node(node["id"], label=node["label"], shape=node["shape"], image=str(Path(node["image"]).resolve()))

        # Ajouter des arêtes
        for node in nodeList:
            for link in node["links"]:
                # si link est vide, on ne fait rien
                if link != []:
                    net.add_edge(node["id"], link)

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
