# from lan_test3 import LanAudacity
import os


files = os.listdir(os.getcwd())
path_project = os.path.join(os.getcwd(), files[8])
print(path_project)

# Dictionnaire contenant les informations
info_dict = {
    'path': 'C:/Users/g.tronche/Documents/test_app/test-v4/db/interfaces'
}

# Extraire le chemin d'accès du dictionnaire
path = info_dict.get('path')

# Afficher le chemin d'accès
print("Chemin d'accès :", path)

# Normaliser le chemin d'accès (pour uniformiser les séparateurs de répertoire)
normalized_path = os.path.normpath(path)

# Vérifier si le chemin d'accès existe
if os.path.exists(normalized_path):
    print("Le chemin d'accès est valide et existe.")
else:
    print("Le chemin d'accès est invalide ou n'existe pas.")

