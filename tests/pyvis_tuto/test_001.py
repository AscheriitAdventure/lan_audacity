import sys
import os
import networkx as nx
from pyvis.network import Network
from qtpy.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from qtpy.QtWebEngineWidgets import QWebEngineView
from qtpy.QtCore import QUrl


class GraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyVis Graph Viewer")
        self.setGeometry(100, 100, 1000, 800)

        self.generate_graph()

        self.browser = QWebEngineView()
        html_path = os.path.abspath("graph/net_map.html")
        self.browser.load(QUrl.fromLocalFile(html_path))

        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def generate_graph(self):
        g = Network(height="750px", width="100%", notebook=False)
        nxg = nx.complete_graph(6)
        g.from_nx(nxg)

        os.makedirs("graph/js", exist_ok=True)
        html_path = "graph/net_map.html"
        g.write_html(html_path)

        # 1. Télécharger le vis-network.min.js localement si manquant
        js_path = "graph/js/vis-network.min.js"
        if not os.path.exists(js_path):
            import urllib.request
            url = "https://unpkg.com/vis-network@9.1.2/dist/vis-network.min.js"
            urllib.request.urlretrieve(url, js_path)

        # 2. Patch le HTML généré pour utiliser vis-network.min.js en local
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Supprimer tout <script src="https://...vis...">
        import re
        html = re.sub(
            r'<script type="text/javascript" src=".*?vis.*?\.js.*?"></script>',
            '<script type="text/javascript" src="js/vis-network.min.js"></script>',
            html
        )

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphWindow()
    window.show()
    sys.exit(app.exec_())
