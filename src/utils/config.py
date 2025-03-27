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

