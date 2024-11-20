import os
import logging
from qtpy.QtWidgets import QApplication
from src.views.templates.FilesViews.filesTextViews import Files2TVU1 as Files2TV  # Assurez-vous que ce chemin est correct


# Fonction pour créer un fichier de test
def create_test_file(file_name: str, content: str) -> str:
    with open(file_name, 'w') as file:
        file.write(content)
    return file_name


if __name__ == "__main__":
    # Configuration de logging
    logging.basicConfig(level=logging.INFO)

    # Création du fichier de test
    test_file_name = 'C:\\Users\g.tronche\Documents\GitHub\lan_audacity\code\src\\functionsExt.py'
    # file_content = "Ceci est un fichier de test.\nIl contient quelques lignes de texte pour vérifier le contenu."
    # create_test_file(test_file_name, file_content)

    # Lancement de l'application Qt
    app = QApplication([])

    # Instanciation de la classe Files2TV avec le chemin du fichier de test
    file_view = Files2TV(file_path=test_file_name)

    # Afficher la fenêtre contenant le fichier
    file_view.setWindowTitle(f"Affichage du fichier: {test_file_name}")
    file_view.resize(800, 600)
    file_view.show()

    # Lancer l'application
    app.exec_()

    # Optionnel: Nettoyage après l'exécution (supprimer le fichier de test)
    if os.path.exists(test_file_name):
        os.remove(test_file_name)
