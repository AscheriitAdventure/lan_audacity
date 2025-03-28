from tests.dynamic_widget import DWG
from tests.dynamic_widget.dyn_data import VAR_TMP_DFT, VAR_N_DB

if __name__ == "__main__":
    import sys
    from qtpy.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Créer le générateur de widgets
    generator = DWG()
    
    # Exemple de dictionnaire de configuration
    config = VAR_N_DB

     # Générer le widget à partir de la configuration
    main_widget = generator.create_widget(config)
    main_widget.show()
    
    sys.exit(app.exec())