#!/bin/bash

# Script pour lancer docker-compose avec l'environnement souhaité

# Vérifier si docker-compose est installé
if ! command -v docker-compose &> /dev/null
then
    echo "Erreur : docker-compose n'est pas installé. Veuillez l'installer avant d'exécuter ce script."
    exit 1
fi

# Vérifier si le fichier .env est présent