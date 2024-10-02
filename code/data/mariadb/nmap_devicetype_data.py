import mysql.connector
import json

# Configuration de la connexion à la base de données
db_config = {
    'host': 'localhost',        # Remplacez par votre hôte
    'user': 'root',             # Remplacez par votre nom d'utilisateur
    'password': 'root',         # Remplacez par votre mot de passe
    'database': 'lan_audacity_sql_server'  # Remplacez par le nom de votre base de données
}

# Lecture des données JSON à partir d'un fichier
chemin = "C:\\Users\\g.tronche\\Documents\\GitHub\\lan_audacity\\code\\data\\nmap_device_type.json"
try:
    with open(chemin, "r", encoding="utf-8") as file:
        data = json.load(file)  # Utilisation de json.load() pour lire à partir d'un fichier

except FileNotFoundError:
    print("Le fichier JSON n'a pas été trouvé.")
    exit(1)
except json.JSONDecodeError:
    print("Erreur lors du décodage du fichier JSON.")
    exit(1)

# Connexion à la base de données
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Requête d'insertion
    insert_query = '''
    INSERT INTO DeviceType (category_name, category_description, osi_layer_id) VALUES (%s, %s, %s)
    '''

    # Exécuter les insertions
    for item in data:
        print(item['name_type'])
        values = (item['name_type'], item['dsc_type'], item['osi_layer'])
        cursor.execute(insert_query, values)

    # Valider les modifications
    connection.commit()
    print(f"{cursor.rowcount} enregistrements insérés avec succès.")

except mysql.connector.Error as err:
    print(f"Erreur : {err}")
finally:
    # Fermer la connexion
    if cursor:
        cursor.close()
    if connection:
        connection.close()
