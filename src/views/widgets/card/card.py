from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
from typing import *
import logging
import inspect


SEC_PARAMS: list = [
    {
        "section": "global",
        "dirty_rect": True,
    },
    {
        "section": "top",
        "dirty_rect": False,
        "is_visible": True,
    },
    {
        "section": "left",
        "dirty_rect": False,
        "is_visible": True,
    },
    {
        "section": "center",
        "dirty_rect": False,
        "is_visible": True,
    },
    {
        "section": "right",
        "dirty_rect": False,
        "is_visible": True,
    },
    {
        "section": "bottom",
        "dirty_rect": False,
        "is_visible": True,
    }
]


class Card_2(QFrame):
    def __init__(self, debug: Optional[bool] = False, parent=None):
        super(Card_2, self).__init__(parent)

        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setLineWidth(10)
        self.setMidLineWidth(5)
        self.setContentsMargins(0, 0, 0, 0)

        # self.setStyleSheet("background-color: #E7E9EB; border-radius: 10px;")

        self.debug = debug
        self.activeSections: Dict[str, Any] = {}
        self.sections: list = SEC_PARAMS
        self.mainLayout: Optional[QLayout] = None

    def initUI(self, rebuild: Optional[bool] = False) -> None:
        if rebuild and self.mainLayout is not None:
            self._clearLayout()
        else:
            self.mainLayout = QGridLayout(self)
            self.setLayout(self.mainLayout)

        self._arrangeWidgets()
        self.markAllDirty()
        self.update()
        self.repaint()

    def setPositionCard(self, pos: str, new_obj: Optional[QWidget] = None) -> None:
        """Sets the position card widget."""
        o_c = self.activeSections.get(pos, None)
        if o_c is not None and o_c != new_obj:
            o_c.setParent(None)

        self.activeSections[pos] = new_obj
        self.sections[self._findSectionIndex(pos)]["dirty_rect"] = True
        self.initUI(rebuild=True)

    def _findSectionIndex(self, section: str) -> int:
        """Find the index of a section in the sections list."""
        for i, sec in enumerate(self.sections):
            if sec["section"] == section:
                return i
        return -1

    def _arrangeWidgets(self):
        """
        Arrange les widgets dans le layout
        """
        for s in self.sections:
            section_name: str = s["section"]
            if section_name in self.activeSections and s["dirty_rect"]:
                if s.get("is_visible", True):
                    self.activeSections[section_name].setVisible(True)
                else:
                    self.activeSections[section_name].setVisible(False)

                if section_name == "top":
                    self.mainLayout.addWidget(
                        self.activeSections["top"], 0, 0, 1, 5, Qt.AlignmentFlag.AlignTop)
                    sep = QFrame()
                    sep.setFrameStyle(QFrame.Shape.HLine | QFrame.Shadow.Raised)
                    sep.setMinimumHeight(2)
                    sep.setStyleSheet("background-color: gray;")
                    self.mainLayout.addWidget(sep, 1, 0, 1, 5)

                elif section_name == "left":
                    self.mainLayout.addWidget(
                        self.activeSections["left"], 2, 0, 1, 1)
                    sep = QFrame()
                    sep.setFrameStyle(QFrame.Shape.VLine | QFrame.Shadow.Raised)
                    sep.setMinimumHeight(2)
                    sep.setStyleSheet("background-color: gray;")
                    self.mainLayout.addWidget(sep, 2, 1, 1, 1)

                elif section_name == "center":
                    self.mainLayout.addWidget(
                        self.activeSections["center"], 2, 2, 1, 1)
                    
                elif section_name == "right":
                    self.mainLayout.addWidget(
                        self.activeSections["right"], 2, 4, 1, 1)
                    sep = QFrame()
                    sep.setFrameStyle(QFrame.Shape.VLine | QFrame.Shadow.Raised)
                    sep.setMinimumHeight(2)
                    sep.setStyleSheet("background-color: gray;")
                    self.mainLayout.addWidget(sep, 2, 3, 1, 1)

                elif section_name == "bottom":
                    self.mainLayout.addWidget(
                        self.activeSections["bottom"], 4, 0, 1, 5)
                    sep = QFrame()
                    sep.setFrameStyle(QFrame.Shape.HLine | QFrame.Shadow.Raised)
                    sep.setMinimumHeight(2)
                    sep.setStyleSheet("background-color: gray;")
                    self.mainLayout.addWidget(sep, 3, 0, 1, 5)

    def getTruePosition(self, widget: QWidget, top_bottom: Optional[str] = None) -> QRectF:
        """Récupère la position absolue du widget dans la fenêtre."""
        vqo = widget.rect()  # Variable QRectF Object
        wdt = vqo.width()   # width
        hgt = vqo.height()  # height
        vpo = widget.pos()  # Variable Position Object
        x = vpo.x()         # x
        y = vpo.y()         # y

        lm, tm, rm, bm = self.mainLayout.getContentsMargins()
        tbm = bm * 0.75 + tm * 0.75  # Top/Bottom Margin
        tbw = self.rect().width()   # Top/Bottom Width

        if top_bottom == "Bottom":
            return QRectF(x-lm, y-0.25*tm, tbw, hgt+tbm)
        elif top_bottom == "Top":
            return QRectF(x-lm, y-tm, tbw, hgt+tbm)
        else:
            return QRectF(x, y, wdt, hgt)

    def markAllDirty(self):
        """Marque toutes les sections comme nécessitant une mise à jour."""
        for section in self.sections:
            section["dirty_rect"] = True
        self.update()

    def markSectionDirty(self, section: str):
        """Marque une section spécifique comme nécessitant une mise à jour."""
        index = self._findSectionIndex(section)
        if index != -1:
            self.sections[index]["dirty_rect"] = True
            self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.markAllDirty()
        self.update()

    def _clearLayout(self):
        """Supprime tous les widgets du layout"""
        if self.mainLayout is None:
            return

        while self.mainLayout.count():
            item = self.mainLayout.takeAt(0)
            if item.widget():
                if item.widget() in self.activeSections.values():
                    item.widget().setParent(None)
                else:
                    item.widget().deleteLater()

    def setAllParts(
            self,
            top: Optional[QWidget] = None,
            left: Optional[QWidget] = None,
            center: Optional[QWidget] = None,
            right: Optional[QWidget] = None,
            bottom: Optional[QWidget] = None):
        """Met à jour tous les widgets d'un coup pour éviter plusieurs rebuilds

        Args:
            top (QWidget, optional): Widget supérieur
            left (QWidget, optional): Widget gauche
            center (QWidget, optional): Widget central
            right (QWidget, optional): Widget droit
            bottom (QWidget, optional): Widget inférieur
        """
        self._clearLayout()

        if top is not None:
            self.setPositionCard("top", top)
        if left is not None:
            self.setPositionCard("left", left)
        if center is not None:
            self.setPositionCard("center", center)
        if right is not None:
            self.setPositionCard("right", right)
        if bottom is not None:
            self.setPositionCard("bottom", bottom)
        self.initUI(rebuild=True)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec_(Qt.DropAction.MoveAction)

    def getPositionWidget(self, pos: str) -> Optional[QWidget]:
        """Returns the widget at the specified position."""
        return self.activeSections.get(pos, None)

