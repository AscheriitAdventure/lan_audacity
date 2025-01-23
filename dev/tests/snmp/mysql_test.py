import mysql.connector

# Connexion avec des paramètres explicites
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="db_lanAudacity",
    charset="utf8mb3",  # Force l'utilisation de utf8mb3
    collation="utf8mb3_general_ci",  # Définit une collation compatible
)

print("Connexion réussie !")
