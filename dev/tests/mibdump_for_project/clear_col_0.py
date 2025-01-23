import csv

def remove_duplicates_with_filter(input_csv, output_csv):
    try:
        # Utiliser un ensemble pour suivre les valeurs uniques de la colonne 0
        seen = set()
        rows = []

        # Lire le fichier CSV d'entrée
        with open(input_csv, mode="r", encoding="utf-8") as infile:
            csv_reader = csv.reader(infile)
            header = next(csv_reader)  # Lire l'en-tête
            rows.append(header)  # Conserver l'en-tête dans les résultats

            for row in csv_reader:
                # Vérifier si la valeur de la colonne 0 correspond au filtre
                if row[0].lower().endswith(('.mib', '.my')) and row[0] not in seen:
                    seen.add(row[0])  # Ajouter la valeur au set
                    rows.append(row)  # Ajouter la ligne aux résultats

        # Écrire les résultats dans un nouveau fichier CSV
        with open(output_csv, mode="w", newline="", encoding="utf-8") as outfile:
            csv_writer = csv.writer(outfile)
            csv_writer.writerows(rows)

        print(f"Fichier sans doublons enregistré dans : {output_csv}")

    except Exception as e:
        print(f"Erreur : {e}")

# Exemple d'utilisation
if __name__ == "__main__":
    input_csv = input("Entrez le chemin du fichier CSV d'entrée : ")
    output_csv = input("Entrez le chemin du fichier CSV de sortie : ")
    remove_duplicates_with_filter(input_csv, output_csv)
