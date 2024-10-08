Voici un fichier `docker-compose.yml` qui configure un environnement avec une base de données MySQL, une base de données MongoDB, et une application Python pour "lan audacity". L'application Python interagit avec les deux bases de données :

```yaml
version: '3.8'

services:
  mysql-db:
    image: mysql:8.0
    container_name: mysql-db
    environment:
      MYSQL_ROOT_PASSWORD: root_password  # Remplacez par votre mot de passe MySQL
      MYSQL_DATABASE: lan_audacity_sql_server
      MYSQL_USER: user
      MYSQL_PASSWORD: user_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - lan_network

  mongodb-db:
    image: mongo:latest
    container_name: mongodb-db
    environment:
      MONGO_INITDB_ROOT_USERNAME: mongo_user
      MONGO_INITDB_ROOT_PASSWORD: mongo_password
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    networks:
      - lan_network

  lan-audacity-app:
    build: ./lan_audacity  # Le répertoire où se trouve votre application Python
    container_name: lan-audacity-app
    command: python app.py
    volumes:
      - ./lan_audacity:/app  # Volume pour permettre de voir les modifications du code
    environment:
      MYSQL_HOST: mysql-db
      MYSQL_DATABASE: lan_audacity_sql_server
      MYSQL_USER: user
      MYSQL_PASSWORD: user_password
      MONGO_HOST: mongodb-db
      MONGO_INITDB_ROOT_USERNAME: mongo_user
      MONGO_INITDB_ROOT_PASSWORD: mongo_password
    ports:
      - "5000:5000"  # Port de l'application Python
    depends_on:
      - mysql-db
      - mongodb-db
    networks:
      - lan_network

networks:
  lan_network:
    driver: bridge

volumes:
  mysql_data:
    driver: local
  mongo_data:
    driver: local
```

### Structure du projet

Vous devez structurer votre projet de manière à ce que Docker puisse construire l'application Python et accéder aux bases de données.

1. **Répertoire du projet :**
   ```
   /project
   ├── docker-compose.yml
   └── lan_audacity
       ├── Dockerfile
       └── app.py
   ```

2. **Dockerfile** pour l'application Python (dans le dossier `lan_audacity`) :

```Dockerfile
# Utilisez une image Python de base
FROM python:3.12

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de l'application
COPY . /app

# Installer les dépendances (ajoutez requirements.txt si nécessaire)
RUN pip install mysql-connector-python pymongo

# Exposer le port de l'application
EXPOSE 5000

# Lancer l'application
CMD ["python", "app.py"]
```

3. **Exemple de `app.py` :**

Ce fichier Python représente l'application "lan audacity" qui se connecte aux deux bases de données.

```python
from flask import Flask
import mysql.connector
import pymongo
import os

app = Flask(__name__)

# Configurations pour MySQL
mysql_config = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST'),
    'database': os.getenv('MYSQL_DATABASE'),
}

# Configurations pour MongoDB
mongo_client = pymongo.MongoClient(
    f"mongodb://{os.getenv('MONGO_INITDB_ROOT_USERNAME')}:{os.getenv('MONGO_INITDB_ROOT_PASSWORD')}@{os.getenv('MONGO_HOST')}:27017/"
)
mongo_db = mongo_client["lan_audacity_mongo_db"]

@app.route('/')
def hello():
    return "Hello from LAN Audacity App!"

# Test MySQL connection
@app.route('/test_mysql')
def test_mysql():
    try:
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        return f"MySQL tables: {tables}"
    except mysql.connector.Error as err:
        return f"Error: {err}"

# Test MongoDB connection
@app.route('/test_mongo')
def test_mongo():
    collections = mongo_db.list_collection_names()
    return f"MongoDB collections: {collections}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Instructions

1. Créez le fichier `docker-compose.yml` dans la racine de votre projet.
2. Créez un dossier `lan_audacity` contenant les fichiers `Dockerfile` et `app.py`.
3. Lancez les services avec la commande :

   ```bash
   docker-compose up --build
   ```

Cela va créer et démarrer 3 services :
- Un conteneur MySQL,
- Un conteneur MongoDB,
- Un conteneur pour votre application Python.

L'application Python sera accessible sur `localhost:5000`, MySQL sur `localhost:3306`, et MongoDB sur `localhost:27017`.