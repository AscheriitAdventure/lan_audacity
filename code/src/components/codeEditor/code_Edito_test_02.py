from qtpy.QtWidgets import *
from src.components.codeEditor.cl_codeEditor_02 import CodeEditorv2
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Créer le widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Créer l'éditeur
        self.editor = CodeEditorv2(parent=self)
        self.editor.addAreaActions(CodeEditorv2.ActionArea.LineNumber)
        
        # Créer les labels pour afficher les informations
        self.position_label = QLabel("Position: Row 1, Col 1")
        self.format_label = QLabel("Format: ASCII")
        
        # Connecter les signaux
        self.editor.cursorLocationChanged.connect(self.update_position)
        # self.editor.characterFormatChanged.connect(self.update_format)
        
        # Ajouter les widgets au layout
        layout.addWidget(self.editor)
        layout.addWidget(self.position_label)
        layout.addWidget(self.format_label)
        
        # Configurer la fenêtre
        self.setWindowTitle("Code Editor Test")
        self.resize(800, 600)
        
        # Ajouter du texte de test
        self.editor.setText("Hello World!\nΓειά σου Κόσμε!\n你好，世界！")

    def update_position(self, row: int, col: int):
        self.position_label.setText(f"Row {row}, Col {col}")
        
    def update_format(self, char_format: str):
        self.format_label.setText(f"{char_format}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())