# Lan Audacity Organisation App

## Prérequis

- 4 Go de RAM
- Une liaison avec internet
- Une session qui autorise l'utilisation de machines virtuel

## Préparation de l'environnement
### Arborescence des fichiers
```bash
lan-audacity
├── .env                          # Variables d'environnement globales (optionnel)
├── docker-compose.yml
├── backup                        # Sauvegardes globales du projet
├── dev                           # Environnement de développement
│   ├── .env.dev                  # Variables d'environnement spécifiques à dev
│   ├── server_mariadb_dev        # Serveur MariaDB en développement
│   │   ├── conf                  # Fichiers de configuration pour MariaDB
│   │   ├── data                  # Données spécifiques à MariaDB
│   │   └── logs                  # Journaux de MariaDB
│   ├── server_mongodb_dev        # Serveur MongoDB en développement
│   │   ├── conf                  # Fichiers de configuration pour MongoDB
│   │   ├── data                  # Données spécifiques à MongoDB
│   │   └── logs                  # Journaux de MongoDB
│   └── lan-audacity_app_dev      # Application "lan-audacity" en développement
│       ├── conf                  # Configuration de l'application
│       ├── data                  # Données persistantes (fichiers générés, etc.)
│       ├── src                   # Code source de l'application en développement
│       └── logs                  # Journaux de l'application en développement
└── prod                          # Environnement de production
    ├── .env.prod                 # Variables d'environnement spécifiques à prod
    ├── server_mariadb_prod       # Serveur MariaDB en production
    │   ├── conf                  # Fichiers de configuration pour MariaDB
    │   ├── data                  # Données spécifiques à MariaDB
    │   └── logs                  # Journaux de MariaDB
    ├── server_mongodb_prod       # Serveur MongoDB en production
    │   ├── conf                  # Fichiers de configuration pour MongoDB
    │   ├── data                  # Données spécifiques à MongoDB
    │   └── logs                  # Journaux de MongoDB
    └── lan-audacity_app_prod     # Application "lan-audacity" en production
        ├── conf                  # Configuration de l'application
        ├── data                  # Données persistantes (fichiers générés, etc.)
        ├── dockerfile
        ├── src                   # Code source de l'application en production
        ├── main.py
        └── logs                  # Journaux de l'application en production
```
### Contenu des fichiers
#### `.env.dev`
Exemple:
```bash
# Variables globales
NETWORK_NAME=lan_audacity_dev_network

# Base de données MariaDB (développement)
MARIADB_HOST=server_mariadb_dev
MARIADB_USER=root
MARIADB_PASSWORD=dev_password
MARIADB_DATABASE=audacity_dev_db
MARIADB_PORT=3306

# Base de données MongoDB (développement)
MONGODB_HOST=server_mongodb_dev
MONGODB_PORT=27017
MONGODB_USER=admin
MONGODB_PASSWORD=dev_password

# Application lan-audacity (développement)
APP_PORT=8080
APP_DEBUG=true
LOG_LEVEL=debug
```
#### `.env.prod`
Exemple:
```bash
# Variables globales
NETWORK_NAME=lan_audacity_prod_network

# Base de données MariaDB (production)
MARIADB_HOST=server_mariadb_prod
MARIADB_USER=root
MARIADB_PASSWORD=prod_password
MARIADB_DATABASE=audacity_prod_db
MARIADB_PORT=3306

# Base de données MongoDB (production)
MONGODB_HOST=server_mongodb_prod
MONGODB_PORT=27017
MONGODB_USER=admin
MONGODB_PASSWORD=prod_password

# Application lan-audacity (production)
APP_PORT=80
APP_DEBUG=false
LOG_LEVEL=info
```
#### `docker-compose.yml`
```yml
version: '3.8'

services:
  mariadb:
    image: mariadb:latest
    env_file:
      - ./dev/.env.dev  # Pour l'environnement de développement
      # - ./prod/.env.prod  # Pour l'environnement de production
    environment:
      MYSQL_ROOT_PASSWORD: ${MARIADB_PASSWORD}
      MYSQL_DATABASE: ${MARIADB_DATABASE}
    volumes:
      - ./dev/server_mariadb_dev/data:/var/lib/mysql
      - ./dev/server_mariadb_dev/conf:/etc/mysql/conf.d
      - ./dev/server_mariadb_dev/logs:/var/log/mysql
    ports:
      - "3306:3306"
    networks:
      - lan_network

  mongodb:
    image: mongo:latest
    env_file:
      - ./dev/.env.dev
      # - ./prod/.env.prod  # Pour l'environnement de production
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGODB_USER}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGODB_PASSWORD}
    volumes:
      - ./dev/server_mongodb_dev/data:/data/db
      - ./dev/server_mongodb_dev/logs:/var/log/mongodb

  lan-audacity-app:
    build: ./dev/lan-audacity_app_dev
    env_file:
      - ./dev/.env.dev
      # - ./prod/.env.prod  # Pour l'environnement de production
    environment:
      APP_PORT: ${APP_PORT}
      LOG_LEVEL: ${LOG_LEVEL}
    ports:
      - "${APP_PORT}:5678"
    volumes:
      - ./dev/lan-audacity_app_dev/src:/app/src
      - ./dev/lan-audacity_app_dev/data:/app/data
      - ./dev/lan-audacity_app_dev/logs:/app/logs
    depends_on:
      - mariadb
      - mongodb
    networks:
      - lan_network

networks:
    lan_network:
        driver: bridge
```
