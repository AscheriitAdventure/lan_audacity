from typing import List, ClassVar, Union
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import logging
import os
import inspect
from pathlib import Path

from .tab import Tab
from src.views.widgets import CodeEditor, QBreadcrumbs


class EditorTab(Tab):

    cursorLocationChanged: ClassVar[Signal] = Signal(int, int)

    def __init__(self, file_path: str = "", debug: bool = False, parent=None):
        super().__init__(parent, Tab.TabType.EDITOR, os.path.basename(
            file_path) if file_path else "Untitled")
        self.file_path = ""
        self.debug = debug
        self.functionBtnList: List[QPushButton] = []

        self.setFilePath(file_path)
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Breadcrumbs
        self.breadcrumbs = QBreadcrumbs(
            self._generatedBtnList(), self.debug, self)
        layout.addWidget(self.breadcrumbs, 0, 0, 1, 1)
        # Actions (Save, Read[On/Off])
        self.actions = QWidget()
        layout.addWidget(self.actions, 0, 2, 1, 1)
        # Code Editor
        self.editor = CodeEditor(parent=self)
        self.editor.addAreaActions(CodeEditor.ActionArea.LineNumber)
        layout.addWidget(self.editor, 1, 0, 1, 3)

        self._loadText()

        # Connect signals
        self.editor.textChanged.connect(self.onTextChanged)

    def setFilePath(self, file_path: str):
        if os.path.exists(file_path):
            self.file_path = Path(os.path.normpath(file_path))
        else:
            self.file_path = ""
            logging.error(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Le fichier n'existe pas")

    def _generatedBtnList(self) -> List[QPushButton]:
        btnList = []
        objPathList = self.file_path.parts
        for i in range(len(objPathList)):
            btn = QPushButton(objPathList[i])
            fontMetrics = QFontMetrics(btn.font())
            btn.setFlat(True)
            btn.setMaximumWidth(fontMetrics.horizontalAdvance(btn.text())+10)
            # Ajoute un tooltip indiquant le chemin absolu
            absPath = os.path.abspath(os.sep.join(objPathList[:i+1]))
            btn.setToolTip(absPath)
            # Ajoute à la liste des boutons
            btnList.append(btn)
        return btnList

    def onTextChanged(self):
        if not self.modified:
            self.modified = True
            if hasattr(self.parent(), "update_tab_title"):
                self.parent().update_tab_title(self)

    def _loadText(self):
        try:
            with open(self.file_path, 'r') as f:
                self.editor.setText(f.read())
        except Exception as e:
            logging.error(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error loading file {self.file_path}: {str(e)}")

    def addFuncBtn(self, btns: Union[QPushButton, List[QPushButton]]):
        if isinstance(btns, list):
            for btn in btns:
                self.functionBtnList.append(btn)
        else:
            self.functionBtnList.append(btns)

