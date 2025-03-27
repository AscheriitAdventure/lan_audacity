#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de configuration et gestion des logs de l'application.
Utilise un fichier de configuration YAML pour définir les formateurs,
gestionnaires et loggers.
"""

import os
import sys
import logging
import logging.config
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Chargement des variables d'environnement depuis .env
load_dotenv()

class LoggerSetup:
    """Classe de configuration du système de logs de l'application."""
    
    def __init__(self, yaml_path=None, default_level=logging.INFO):
        """
        Initialise la configuration du logger.
        
        Args:
            yaml_path (str, optional): Chemin vers le fichier de configuration YAML.
                Si None, utilise le chemin par défaut.
            default_level (int, optional): Niveau de log par défaut si la configuration échoue.
        """
        self.default_level = default_level
        
        # Définir le chemin par défaut si non fourni
        if yaml_path is None:
            # Chemin relatif au dossier du projet
            base_dir = Path(__file__).resolve().parent.parent.parent
            self.yaml_path = os.path.join(base_dir, "config", "logs.yaml")
        else:
            self.yaml_path = yaml_path
            
        # Définir les variables d'environnement par défaut si non définies
        self._set_default_env_variables()
        
        # Configurer le logger
        self.setup_logging()
        
    def _set_default_env_variables(self):
        """Définit les variables d'environnement par défaut si elles ne sont pas déjà définies."""
        if not os.getenv("LOG_LEVEL"):
            os.environ["LOG_LEVEL"] = "INFO"
            
        if not os.getenv("APP_LOG"):
            # Définir un chemin par défaut pour le fichier de log
            base_dir = Path(__file__).resolve().parent.parent.parent
            log_dir = os.path.join(base_dir, "logs")
            
            # Créer le dossier logs s'il n'existe pas
            os.makedirs(log_dir, exist_ok=True)
            
            os.environ["APP_LOG"] = os.path.join(log_dir, "app.log")
    
    def _expand_env_vars(self, config_dict):
        """
        Remplace les variables d'environnement dans le dictionnaire de configuration.
        
        Args:
            config_dict (dict): Dictionnaire de configuration à modifier
            
        Returns:
            dict: Dictionnaire avec les variables d'environnement remplacées
        """
        for key, value in config_dict.items():
            if isinstance(value, dict):
                self._expand_env_vars(value)
            elif isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                env_var = value[2:-1]
                config_dict[key] = os.getenv(env_var, "")
        return config_dict
    
    def setup_logging(self):
        """
        Configure le système de logging basé sur le fichier YAML.
        """
        try:
            if os.path.exists(self.yaml_path):
                with open(self.yaml_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    
                    # Remplacer les variables d'environnement dans la configuration
                    config = self._expand_env_vars(config)
                    
                    # Configurer le logging
                    logging.config.dictConfig(config)
                    
                    # Capture des exceptions non gérées
                    sys.excepthook = self._handle_exception
            else:
                # Configuration de base si le fichier n'existe pas
                logging.basicConfig(level=self.default_level)
                logging.warning(f"Le fichier de configuration {self.yaml_path} n'existe pas. Configuration par défaut utilisée.")
        except Exception as e:
            # En cas d'erreur, utiliser une configuration basique
            logging.basicConfig(level=self.default_level)
            logging.error(f"Erreur lors de la configuration du logger: {e}")
    
    def _handle_exception(self, exc_type, exc_value, exc_traceback):
        """
        Gère les exceptions non capturées en les enregistrant dans les logs.
        
        Args:
            exc_type: Type d'exception
            exc_value: Valeur de l'exception
            exc_traceback: Traceback de l'exception
        """
        if issubclass(exc_type, KeyboardInterrupt):
            # Ignore les interruptions clavier
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        logging.error("Exception non gérée:", exc_info=(exc_type, exc_value, exc_traceback))


# Fonction pratique pour obtenir un logger configuré
def get_logger(name):
    """
    Retourne un logger configuré pour le module spécifié.
    
    Args:
        name (str): Nom du module ou du composant (généralement __name__)
        
    Returns:
        logging.Logger: Logger configuré
    """
    return logging.getLogger(name)


# Initialisation du logger au chargement du module
logger_setup = LoggerSetup()

# Logger principal de l'application
app_logger = get_logger('app')

# Pour compatibilité avec le code existant
def configure_logs(yaml_path=None):
    """
    Configure le système de logging de l'application.
    Fonction de compatibilité pour le code existant.
    
    Args:
        yaml_path (str, optional): Chemin vers le fichier de configuration YAML.
    """
    global logger_setup
    logger_setup = LoggerSetup(yaml_path)
    return logger_setup
