import os
import logging
import subprocess
import inspect
from pathlib import Path
from dotenv import load_dotenv

# Variables d'environnement
VAR_GLOBAL_ENV = ".env"
VAR_DEV_ENV = ".env.dev"

# Ressources Git nécessaires
GIT_REPOSITORIES = [
    "https://github.com/ecceman/affinity.git",
    "https://github.com/trevoro/snmp-mibs.git"
]

def load_env_vars():
    """
    Charge les variables d'environnement à partir des fichiers .env
    Le fichier .env.dev a priorité sur le fichier .env global
    """
    # Chargement des variables d'environnement globales
    global_loaded = load_dotenv(VAR_GLOBAL_ENV)
    
    # Chargement des variables d'environnement de développement (prioritaires)
    dev_loaded = load_dotenv(VAR_DEV_ENV, override=True)
    
    # Journalisation du résultat
    if global_loaded:
        logging.debug(f"{inspect.currentframe().f_code.co_name}: Variables d'environnement globales chargées depuis {VAR_GLOBAL_ENV}")
    else:
        logging.warning(f"{inspect.currentframe().f_code.co_name}: Fichier {VAR_GLOBAL_ENV} non trouvé ou vide")

    if dev_loaded:
        logging.debug(f"{inspect.currentframe().f_code.co_name}: Variables d'environnement de développement chargées depuis {VAR_DEV_ENV}")
    else:
        logging.info(f"{inspect.currentframe().f_code.co_name}: Fichier {VAR_DEV_ENV} non trouvé ou vide - utilisation des paramètres de production")

    return global_loaded or dev_loaded

def load_resources():
    """
    Télécharge les ressources Git nécessaires dans le dossier assets.
    Chaque dépôt est cloné dans un sous-dossier portant son nom.
    """
    # Vérifier si git est disponible
    try:
        subprocess.run(['git', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        logging.error(f"{inspect.currentframe().f_code.co_name}: Git n'est pas disponible. Impossible de télécharger les ressources.")
        return False
    
    # Créer le dossier assets s'il n'existe pas
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    
    # Cloner ou mettre à jour chaque dépôt
    for repo_url in GIT_REPOSITORIES:
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = assets_dir / repo_name
        
        if repo_path.exists():
            # Si le dépôt existe déjà, essayer de le mettre à jour
            logging.info(f"{inspect.currentframe().f_code.co_name}: Le dépôt {repo_name} existe déjà, tentative de mise à jour...")
            try:
                subprocess.run(['git', '-C', str(repo_path), 'pull'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                logging.info(f"{inspect.currentframe().f_code.co_name}: Dépôt {repo_name} mis à jour.")
            except subprocess.SubprocessError as e:
                logging.warning(f"{inspect.currentframe().f_code.co_name}: Impossible de mettre à jour {repo_name}: {e}")
        else:
            # Cloner le dépôt
            logging.info(f"{inspect.currentframe().f_code.co_name}: Téléchargement du dépôt {repo_name}...")
            try:
                subprocess.run(['git', 'clone', repo_url, str(repo_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                logging.info(f"{inspect.currentframe().f_code.co_name}: Dépôt {repo_name} téléchargé avec succès.")
            except subprocess.SubprocessError as e:
                logging.error(f"{inspect.currentframe().f_code.co_name}: Erreur lors du téléchargement de {repo_name}: {e}")
    
    return True

def verify_resources():
    """
    Vérifie que les ressources nécessaires sont présentes dans le dossier assets.
    
    Returns:
        bool: True si toutes les ressources sont présentes, False sinon
    """
    assets_dir = Path("assets")
    
    if not assets_dir.exists():
        logging.error(f"{inspect.currentframe().f_code.co_name}: Le dossier assets n'existe pas.")
        return False
    
    all_resources_present = True
    
    for repo_url in GIT_REPOSITORIES:
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = assets_dir / repo_name
        
        if not repo_path.exists():
            logging.error(f"{inspect.currentframe().f_code.co_name}: La ressource {repo_name} est manquante.")
            all_resources_present = False
    
    if all_resources_present:
        logging.info(f"{inspect.currentframe().f_code.co_name}: Toutes les ressources sont présentes.")
    else:
        logging.warning(f"{inspect.currentframe().f_code.co_name}: Certaines ressources sont manquantes.")
    
    return all_resources_present

def get_resource_path(repo_name, *subpaths):
    """
    Construit le chemin vers une ressource spécifique dans un dépôt cloné.
    
    Args:
        repo_name (str): Nom du dépôt (sans .git)
        *subpaths: Chemins supplémentaires à ajouter
        
    Returns:
        Path: Chemin complet vers la ressource
    """
    base_path = Path("assets") / repo_name
    return base_path.joinpath(*subpaths)

def prettyKeys(obj: object) -> dict:
    """
    renvoi un dictionnaire de joli clefs ex:
        entrée object
            {'attribut1': 'Hello', '_HW__attribut2': 'World', '_HW__attribut3': '!'}
        sortie {'attribut1': 'Attribut 1', '_HW__attribut2': 'Attribut 2', '_HW__attr33ibut': 'Attr 33 Ibut'}
    """
    origin_d = obj.__dict__
    tmp_d: dict = {}

    for k, v in origin_d.items():
        original_key = k
        new_value = k

        if obj.__class__.__name__ in new_value:
            # Suppression du nom de la classe
            new_value = new_value.replace(f"_{obj.__class__.__name__}", "")

        # Si le nom de la variable commence par un ou plusieurs underscore, on les supprime
        new_value = new_value.lstrip('_')

        # Si le nom de la variable possède un ou plusieurs underscore, on les remplace par un espace
        new_value = new_value.replace('_', ' ')

        # Si le nom de la variable possède des chiffres collés à une suite de lettres,
        # on ajoute un espace entre les lettres et les chiffres
        import re
        new_value = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', new_value)
        new_value = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', new_value)

        # Pour finir tous les mots > 2 lettres commencent par une majuscule
        words = new_value.split()
        capitalized_words = []

        for word in words:
            if len(word) > 2:
                capitalized_words.append(word.capitalize())
            else:
                capitalized_words.append(word)

        # Ajouter un espace avant les chiffres à la fin
        base_name = ''.join(capitalized_words)
        # Extraire les chiffres à la fin du nom
        match = re.search(r'(\d+)$', original_key)
        if match:
            number = match.group(1)
            base_name = re.sub(r'\d+$', '', base_name)
            new_value = f"{base_name} {number}"
        else:
            # Si pas de chiffre à la fin, vérifier si on peut en trouver dans le nom
            match = re.search(r'(\d+)', original_key)
            if match:
                number = match.group(1)
                parts = re.split(r'\d+', base_name, maxsplit=1)
                if len(parts) > 1:
                    new_value = f"{parts[0]} {number} {parts[1]}"
                else:
                    new_value = f"{parts[0]} {number}"
            else:
                # Si pas de chiffres du tout, ajouter l'index de la clé
                index = list(origin_d.keys()).index(original_key) + 1
                new_value = f"{base_name} {index}"

        tmp_d[original_key] = new_value

    return tmp_d

def prettyKeysList(obj: object) -> list:
    """
    Renvoie une liste de jolies clés formatées à partir des attributs d'un objet.
    
    Exemple:
        entrée object avec dict:
            {'attribut1': 'Hello', '_HW__attribut2': 'World', '_HW__attribut3': '!'}
        sortie:
            ['Attribut 1', 'Attribut 2', 'Attribut 3']
    """
    origin_d = obj.__dict__
    pretty_keys = []
    
    for k in origin_d.keys():
        new_value = k
        
        if obj.__class__.__name__ in new_value:
            # Suppression du nom de la classe
            new_value = new_value.replace(f"_{obj.__class__.__name__}", "")
        
        # Si le nom de la variable commence par un ou plusieurs underscore, on les supprime
        new_value = new_value.lstrip('_')
        
        # Si le nom de la variable possède un ou plusieurs underscore, on les remplace par un espace
        new_value = new_value.replace('_', ' ')
        
        # Si le nom de la variable possède des chiffres collés à une suite de lettres,
        # on ajoute un espace entre les lettres et les chiffres
        import re
        new_value = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', new_value)
        new_value = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', new_value)
        
        # Pour finir tous les mots > 2 lettres commencent par une majuscule
        words = new_value.split()
        capitalized_words = []
        
        for word in words:
            if len(word) > 2:
                capitalized_words.append(word.capitalize())
            else:
                capitalized_words.append(word)
        
        # Ajouter un espace avant les chiffres à la fin
        base_name = ''.join(capitalized_words)
        # Extraire les chiffres à la fin du nom
        match = re.search(r'(\d+)$', k)
        if match:
            number = match.group(1)
            base_name = re.sub(r'\d+$', '', base_name)
            new_value = f"{base_name} {number}"
        else:
            # Si pas de chiffre à la fin, vérifier si on peut en trouver dans le nom
            match = re.search(r'(\d+)', k)
            if match:
                number = match.group(1)
                parts = re.split(r'\d+', base_name, maxsplit=1)
                if len(parts) > 1:
                    new_value = f"{parts[0]} {number} {parts[1]}"
                else:
                    new_value = f"{parts[0]} {number}"
            else:
                # Si pas de chiffres du tout, ajouter l'index de la clé
                index = list(origin_d.keys()).index(k) + 1
                new_value = f"{base_name} {index}"
        
        pretty_keys.append(new_value)
        
    return pretty_keys
