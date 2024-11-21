from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
from typing import *
import logging


class LineIntArea(QWidget):
    def __init__(
            self, 
            editor, # CodeEditorView
            parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.editor = editor
    
    def sizeHint(self) -> QSize:
        return QSize(self.editor.lineIntAreaWidth(), 0)
    
    def paintEvent(self, event):
        self.editor.rowAreaPaintEvent(event)
        