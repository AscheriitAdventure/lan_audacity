from dev.project.src.classes.cl_dialog import DynFormDialog
from dev.project.src.lib.template_dialog import *
import sys
import os
from qtpy.QtWidgets import QApplication
from qtpy.QtCore import Qt

def main():
    # Création de l'application Qt
    app = QApplication(sys.argv)

    # Création et affichage du dialogue
    try:
        dialog = DynFormDialog(debug=False)
        dialog.load_form(NEW_PROJECT)
        
        # Attendre que le dialogue soit fermé
        if dialog.exec():
            data = dialog.get_form_data()
            print(f"Données entrées : {data}")
        else:
            print("Dialogue annulé")
            
    except Exception as e:
        print(f"Erreur : {str(e)}")
        
    # Nettoyage et sortie
    sys.exit(app.exec())

if __name__ == '__main__':
    main()