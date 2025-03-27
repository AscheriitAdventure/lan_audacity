from typing import List
from dotenv import load_dotenv
from pathlib import Path
import logging
import inspect
import os
import sys


class ScanApp:
    def __init__(self, app_path: str, debug: bool = False):
        self.__debug = debug
        self.__env_files: List[str] = []
        self.__app_path: Path = Path(app_path)
        
        # Configuration du logging
        self.__logger = logging.getLogger(__name__)
        # Supprimer les handlers existants pour éviter les duplications
        if self.__logger.handlers:
            self.__logger.handlers.clear()
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)
        
        # Définir le niveau de logging selon le mode debug
        if self.__debug:
            self.__logger.setLevel(logging.DEBUG)
        else:
            self.__logger.setLevel(logging.INFO)
    
    @property
    def debug(self) -> bool:
        return self.__debug
    
    @debug.setter
    def debug(self, var: bool) -> None:
        self.__debug = var
        # Mise à jour du niveau de logging quand debug change
        if var:
            self.__logger.setLevel(logging.DEBUG)
        else:
            self.__logger.setLevel(logging.INFO)
    
    @property
    def envFiles(self) -> List[str]:
        return self.__env_files
    
    def addEnvFile(self, var: str) -> None:
        self.__env_files.append(var)
    
    @property
    def appPath(self) -> Path:
        return self.__app_path.absolute()
    
    def scanEnvFiles(self) -> List[Path]:
        """
        Cherche tous les fichiers .env et .env.* dans le dossier de l'application
        et les ajoute à la liste des fichiers d'environnement.
        
        Returns:
            List[Path]: Liste des chemins des fichiers trouvés
        """
        self.__logger.debug(f"Recherche des fichiers d'environnement dans {self.appPath}")
        
        if not self.appPath.exists():
            err_msg = f"Le chemin de l'application n'existe pas: {self.appPath}"
            self.__logger.error(err_msg)
            sys.exit(1)
            
        env_paths = []
        
        # Chercher tous les fichiers .env et .env.*
        for file in self.appPath.glob('.env*'):
            if file.is_file():
                self.__logger.debug(f"Fichier d'environnement trouvé: {file}")
                env_paths.append(file)
                self.addEnvFile(str(file))
        
        if not env_paths:
            self.__logger.warning(f"Aucun fichier d'environnement trouvé dans {self.appPath}")
            
        return env_paths
    
    def validateEnvLinks(self, env_paths: List[Path]) -> bool:
        """
        Vérifie que tous les liens dans les fichiers d'environnement existent.
        Se concentre sur les chemins de fichiers relatifs qui sont susceptibles d'être
        des ressources nécessaires à l'application.
        
        Args:
            env_paths (List[Path]): Liste des chemins des fichiers d'environnement
            
        Returns:
            bool: True si tous les liens sont valides, False sinon
        """
        self.__logger.debug("Validation des liens dans les fichiers d'environnement")
        
        # Extensions de fichiers à vérifier
        file_extensions = ['.yaml', '.yml', '.json', '.db', '.log', '.py', '.txt', '.csv', '.ini', '.cfg']
        # Dossiers à vérifier
        folder_keywords = ['path', 'dir', 'directory', 'folder', 'lib', 'library']
        
        for env_path in env_paths:
            try:
                with open(env_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                for line_num, line in enumerate(lines, 1):
                    line = line.strip()
                    # Ignorer les commentaires et les lignes vides
                    if not line or line.startswith('#'):
                        continue
                    
                    # Vérifier s'il y a une assignation de variable
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Ignorer les valeurs qui sont des listes, URLs, ou autres types non-fichiers
                        if value.startswith('[') or value.startswith('http') or value.startswith('{'):
                            continue
                            
                        # Enlever les guillemets si présents
                        if (value.startswith('"') and value.endswith('"')) or \
                           (value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]
                        
                        # Vérifier si c'est un chemin absolu ou un chemin relatif
                        is_path = False
                        
                        # Chemins absolus
                        if value.startswith('/') or ':/' in value or ':\\' in value:
                            is_path = True
                        # Chemins relatifs explicites
                        elif value.startswith('./') or value.startswith('../'):
                            is_path = True
                        # Fichiers avec extensions à vérifier
                        elif any(value.endswith(ext) for ext in file_extensions):
                            is_path = True
                        # Variables qui semblent désigner des dossiers
                        elif any(keyword in key.lower() for keyword in folder_keywords):
                            is_path = True
                        
                        if is_path:
                            path = Path(value)
                            
                            # Si le chemin est relatif, le rendre absolu par rapport au dossier de l'application
                            if not path.is_absolute():
                                path = (self.appPath / path).resolve()
                            
                            if not path.exists():
                                err_msg = f"Lien invalide dans {env_path}, ligne {line_num}: {value} n'existe pas"
                                self.__logger.error(err_msg)
                                return False
                            else:
                                self.__logger.debug(f"Lien valide dans {env_path}: {value}")
            
            except Exception as e:
                err_msg = f"Erreur lors de la lecture de {env_path}: {str(e)}"
                self.__logger.error(err_msg)
                return False
                
        return True
    
    def generateEnvironment(self):
        """
        Charge les variables d'environnement à partir des fichiers .env trouvés
        et crée les répertoires nécessaires s'ils n'existent pas
        """
        env_paths = self.scanEnvFiles()
        
        if not env_paths:
            self.__logger.warning("Aucun fichier d'environnement à charger")
            return
        
        # Vérifier que tous les liens sont valides
        if not self.validateEnvLinks(env_paths):
            err_msg = "Des liens invalides ont été trouvés dans les fichiers d'environnement"
            self.__logger.error(err_msg)
            sys.exit(1)
        
        # Charger les variables d'environnement
        for env_path in env_paths:
            self.__logger.info(f"Chargement des variables d'environnement depuis {env_path}")
            load_dotenv(dotenv_path=env_path, override=True)
        
        # Traiter les variables spécifiques après le chargement
        self.__process_loaded_env_vars()
        
        self.__logger.debug("Variables d'environnement chargées avec succès")
        
    def __process_loaded_env_vars(self):
        """
        Traite les variables d'environnement spécifiques après leur chargement
        pour assurer que les répertoires nécessaires existent
        """
        # Cherche les variables qui pourraient être des chemins de dossiers
        folder_keywords = ['_DIR', '_PATH', 'DIRECTORY', '_FOLDER']
        dirs_to_create = []
        
        for key, value in os.environ.items():
            # Vérifier si c'est une variable de chemin
            if any(keyword in key for keyword in folder_keywords) and value:
                # Ignorer les URLs et les valeurs qui ne sont pas des chemins
                if value.startswith('http') or value.startswith('['):
                    continue
                    
                # Enlever les guillemets si présents
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                
                path = Path(value)
                
                # Si le chemin est relatif, le rendre absolu par rapport au dossier de l'application
                if not path.is_absolute():
                    path = (self.appPath / path).resolve()
                
                # Si c'est un dossier et qu'il n'existe pas, l'ajouter à la liste à créer
                if not path.exists() and not path.suffix:  # Pas d'extension = probablement un dossier
                    dirs_to_create.append(path)
        
        # Créer les répertoires manquants
        for dir_path in dirs_to_create:
            try:
                self.__logger.info(f"Création du répertoire: {dir_path}")
                dir_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                self.__logger.warning(f"Impossible de créer le répertoire {dir_path}: {str(e)}")
                