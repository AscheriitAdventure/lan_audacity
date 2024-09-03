import os, string

def get_file_format(abs_path: str) -> str:
    _, file_extension = os.path.splitext(abs_path)
    return file_extension.lower().strip(string.punctuation)  # retourne l'extension en minuscules

# Exemple d'utilisation :
abs_path = "/chemin/vers/le/fichier.txt"
file_format = get_file_format(abs_path)
print("Format du fichier:", file_format)
