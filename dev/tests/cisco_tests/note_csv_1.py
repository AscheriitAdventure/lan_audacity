import sys
import pandas as pd
from qtpy.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QFileDialog, QPushButton, QVBoxLayout, QWidget
from pysnmp.smi import builder, view, compiler
from pysnmp.smi.rfc1902 import ObjectIdentity


START_OID = "1.3.6.1.2"

class OidTreeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Affichage des OID (mib-2)")
        self.setGeometry(100, 100, 800, 500)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 🔘 Bouton pour ouvrir le fichier CSV
        self.load_button = QPushButton("📂 Sélectionner un fichier CSV")
        self.load_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.load_button)

        # 🌳 QTreeWidget pour afficher les OIDs
        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(3)  # Colonnes : OID, Name (dernier label), Description complète
        self.tree.setHeaderLabels(["OID", "Name", "Description"])
        self.layout.addWidget(self.tree)

    def open_file_dialog(self):
        """ Ouvre une boîte de dialogue pour sélectionner un fichier CSV """
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Sélectionner un fichier CSV", "", "Fichiers CSV (*.csv)")

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
            for _, row in df.iterrows():
                full_oid = str(row["OID"])
                full_desc = str(row["DSC"])
                short_name = str(row["TXT-END"])

                # Ignorer les entrées où TXT-END est "#N/A"
                if short_name == "nan":
                    # print(f"⚠️ Entrée ignorée : OID={full_oid}, Description={full_desc}")
                    # passer à l'iteration suivante
                    continue
                
                relative_oid = full_oid[len(START_OID) + 1:]  # Supprime "1.3.6.1.2."

                oid_parts = relative_oid.split(".")  # Découpage de l'OID
                parent = self.tree
                oid_path = START_OID  # Commencer à mib-2
                for part in oid_parts:
                    oid_path += "." + part
                    if oid_path not in oid_dict:
                        item = QTreeWidgetItem(parent, [oid_path, "", ""])  # Ajout de 3 colonnes
                        oid_dict[oid_path] = item
                    parent = oid_dict[oid_path]

                parent.setText(1, short_name)  # 🆕 Nom (dernier label)
                parent.setText(2, full_desc)   # 🔎 Description complète

        except Exception as e:
            print(f"⚠️ Erreur lors de la lecture du fichier CSV : {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OidTreeApp()
    window.show()
    sys.exit(app.exec())
