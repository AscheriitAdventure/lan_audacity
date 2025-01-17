import sys
import pandas as pd
from qtpy.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QFileDialog, QPushButton, QVBoxLayout, QWidget

START_OID = "1.3.6.1.2"  # mgmt

class OidTreeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Affichage des OID (mib-2)")
        self.setGeometry(100, 100, 800, 500)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Bouton pour ouvrir le fichier CSV
        self.load_button = QPushButton("📂 Sélectionner un fichier CSV")
        self.load_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.load_button)

        # QTreeWidget pour afficher uniquement les OIDs
        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["OID"])
        self.layout.addWidget(self.tree)

    def open_file_dialog(self):
        """ Ouvre une boîte de dialogue pour sélectionner un fichier CSV """
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Sélectionner un fichier CSV", "", "Fichiers CSV (*.csv)")

        if file_path:
            self.load_csv_data(file_path)

    def load_csv_data(self, file_path):
        """ Charge les OID depuis un fichier CSV et affiche ceux à partir de mib-2 """
        try:
            df = pd.read_csv(file_path, dtype=str)

            # Vérifier que la colonne OID existe
            if "OID" not in df.columns:
                print("⚠️ Le fichier CSV doit contenir une colonne 'OID'.")
                return

            # Filtrer les OIDs commençant par mib-2
            df = df[df["OID"].str.startswith(START_OID)]

            oid_dict = {}
            for oid in df["OID"]:
                relative_oid = oid[len(START_OID) + 1:]
                oid_parts = relative_oid.split(".")
                parent = self.tree
                oid_path = START_OID
                
                for part in oid_parts:
                    oid_path += "." + part
                    if oid_path not in oid_dict:
                        item = QTreeWidgetItem(parent, [oid_path])
                        oid_dict[oid_path] = item
                    parent = oid_dict[oid_path]

        except Exception as e:
            print(f"⚠️ Erreur lors de la lecture du fichier CSV : {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OidTreeApp()
    window.show()
    sys.exit(app.exec())
