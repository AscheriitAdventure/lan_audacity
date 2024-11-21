from qtpy.QtWidgets import QApplication
# from src.components.codeEditor.cl_codeEditor import CodeEditorView as CodeEditor
from src.views.templates.FilesViews.dev_codeEditor import CodeEditor
import os


path = os.path.normpath("C:/Users/g.tronche/Documents/GitHub/lan_audacity/code/data/navBar_obj.json")
with open(path, 'r', encoding='utf-8') as file:
    file_content = file.read()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    editor = CodeEditor()
    editor.setText(file_content)
    editor.resize(400, 300)
    editor.show()
    sys.exit(app.exec_())
