import os
import logging
import inspect

def get_app_name():
    """Récupère le nom de l'application depuis les variables d'environnement"""
    return os.getenv("APP_NAME", "Mon Application MVC")

def get_app_version():
    """Récupère la version de l'application depuis les variables d'environnement"""
    return os.getenv("APP_VERSION", "1.0.0")

def get_app_organization():
    """Récupère l'organisation depuis les variables d'environnement"""
    return os.getenv("APP_ORGANIZATION", "Mon Organisation")

def log_function_call(message):
    """Journalise un message avec le nom de la fonction appelante"""
    caller_frame = inspect.currentframe().f_back
    function_name = caller_frame.f_code.co_name
    logging.info(f"{function_name}: {message}")

def load_resources():
    """
    Charge les ressources externes si nécessaire
    Par exemple: cloner des dépôts Git, télécharger des fichiers, etc.
    """
    resources_dir = "assets"
    
    # Créer le répertoire des ressources s'il n'existe pas
    if not os.path.exists(resources_dir):
        os.makedirs(resources_dir, exist_ok=True)
        log_function_call(f"Répertoire de ressources créé: {resources_dir}")
    
    # Exemple: vérification des ressources requises
    required_resources = ["icons", "styles"]
    for resource in required_resources:
        resource_path = os.path.join(resources_dir, resource)
        if not os.path.exists(resource_path):
            os.makedirs(resource_path, exist_ok=True)
            log_function_call(f"Sous-répertoire de ressources créé: {resource_path}")