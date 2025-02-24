from qtpy.QtWidgets import QApplication
from src.components.codeEditor.cl_codeEditor import CEVU1 as CodeEditor
import os

# Fonction pour créer un fichier de test
def create_test_file(file_name: str, content: str) -> str:
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)
    return file_name

test_file_name = "read.txt"
file_content = "Ceci est un fichier de test.\nIl contient quelques lignes de texte pour vérifier le contenu."
create_test_file(test_file_name, file_content)


# path = os.path.normpath("C:/Users/g.tronche/Documents/GitHub/lan_audacity/code/data/navBar_obj.json")
path = os.path.normpath(test_file_name)
with open(path, 'r', encoding='utf-8') as file:
    file_content = file.read()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    editor = CodeEditor()
    editor.setPlainText(file_content)
    editor.resize(400, 300)
    editor.show()
    sys.exit(app.exec_())
