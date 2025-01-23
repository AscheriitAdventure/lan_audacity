import os
import csv

def search_and_write_csv(input_dir, output_dir, search_string):
    try:
        # Vérifier si les chemins existent
        if not os.path.isdir(input_dir):
            raise FileNotFoundError(f"Le dossier de recherche '{input_dir}' n'existe pas.")
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
            print(f"Le dossier d'écriture '{output_dir}' a été créé.")

        # Nom du fichier de sortie
        output_file = os.path.join(output_dir, "resultats_recherche.csv")

        # Créer le fichier CSV et écrire l'en-tête
        with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Chemin du fichier", "Numéro de ligne", "Contenu de la ligne"])

            # Parcourir les fichiers du dossier de recherche
            for root, _, files in os.walk(input_dir):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    try:
                        # Lire le contenu du fichier
                        with open(file_path, "r", encoding="utf-8") as infile:
                            lines = infile.readlines()

                        # Rechercher la chaîne et enregistrer les correspondances
                        for line_number, line in enumerate(lines, start=1):
                            if search_string in line:
                                csv_writer.writerow([file_path, line_number, line.strip()])
                                # print(f"{file_path} - Ligne {line_number}: {line.strip()}")  # Affiche le résultat dans la console

                    except Exception as e:
                        print(f"Impossible de lire le fichier '{file_path}': {e}")

        print(f"\nRecherche terminée. Résultats enregistrés dans '{output_file}'.")
    except Exception as e:
        print(f"Erreur : {e}")

# Exemple d'utilisation
if __name__ == "__main__":
    input_dir = input("Entrez le chemin du dossier de recherche : ")
    output_dir = input("Entrez le chemin du dossier d'écriture : ")
    search_string = input("Entrez la suite de caractères à chercher : ")
    search_and_write_csv(input_dir, output_dir, search_string)
