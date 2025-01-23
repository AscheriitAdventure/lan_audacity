import pandas as pd

# Chemin du fichier CSV
file_path = r"D:/lan_audacity/dev/tests/mibdump_for_project/resultats_recherche.csv"

# Charger le fichier CSV
try:
    df = pd.read_csv(file_path)
    
    # Garder uniquement la première colonne (colonne 0)
    if not df.empty:
        column_0 = df.iloc[:, [0]]  # Sélectionner uniquement la colonne 0
        
        # Sauvegarder le résultat dans le même fichier ou un autre fichier si nécessaire
        output_path = r"D:/lan_audacity/dev/tests/mibdump_for_project/colonne_0_resultats.csv"
        column_0.to_csv(output_path, index=False)
        output_path
    else:
        "Le fichier CSV est vide."
except FileNotFoundError:
    "Le fichier spécifié est introuvable."
except Exception as e:
    str(e)
