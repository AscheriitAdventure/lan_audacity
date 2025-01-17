import sys
import pandas as pd
from qtpy.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QFileDialog, QPushButton, QVBoxLayout, QWidget
from pysnmp.smi import builder, view, compiler
from pysnmp.smi.rfc1902 import ObjectIdentity

# 📌 Chemin vers le dossier contenant les MIBs convertis en .py
MIB_PATH = 'D:/lan_audacity/backup/dev/py_mibs'
START_OID = "1.3.6.1.2"  # Filtrer à partir de mib-2

# 🔹 Charger les fichiers MIB
mibBuilder = builder.MibBuilder()
mibBuilder.add_mib_sources(builder.DirMibSource(MIB_PATH))
compiler.add_mib_compiler(mibBuilder, sources=['http://mibs.snmplabs.com/asn1/@mib@', f'file://{MIB_PATH}'])

# 🔹 Charger les modules MIB nécessaires
mib_list = [
    'SNMPv2-MIB', 'IP-MIB', 'IP-FORWARD-MIB', 'IF-MIB', 'DISMAN-EXPRESSION-MIB',
    'DISMAN-EVENT-MIB', 'RFC1213-MIB', 'EtherLike-MIB', 'RMON-MIB', 'RMON2-MIB',
    'SMON-MIB', 'BRIDGE-MIB', 'POWER-ETHERNET-MIB'
]
for mib in mib_list:
    try:
        mibBuilder.load_modules(mib)
    except Exception as e:
        print(f"⚠️ Erreur lors du chargement du module {mib} : {e}")

# 🔹 Construire un traducteur
mibViewController = view.MibViewController(mibBuilder)


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

    def resolve_oid(self, oid):
        """ Essaie de trouver le nom lisible de l'OID avec la MIB """
        try:
            obj_lab = ObjectIdentity(oid)
            obj_lab.resolve_with_mib(mibViewController)
            full_name = ".".join(map(str, obj_lab.get_label()))  # Nom complet
            short_name = obj_lab.get_label()[-1]  # Dernier label
            return full_name, short_name
        except Exception:
            return "N/A", "N/A"

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
                full_oid = row["OID"]
                full_desc, short_name = self.resolve_oid(full_oid)  # 🔎 Résolution du nom lisible via MIB

                # Supprimer le préfixe "1.3.6.1.2" pour ne pas l'afficher plusieurs fois
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
