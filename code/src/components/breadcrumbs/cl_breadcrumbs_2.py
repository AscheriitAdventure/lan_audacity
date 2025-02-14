import typing
import enum
from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
import logging
import inspect
import sys
from typing import List, Union, Optional, Any, ClassVar


class QBreadcrumbs(QWidget):
    class Orientation(enum.Enum):
        """Enum for breadcrumb orientation options"""
        HORIZONTAL = 1
        VERTICAL = 2

    class ReadingDirection(enum.Enum):
        """Enum for breadcrumb reading direction options"""
        LeftToRight = 0
        RightToLeft = 1
        TopToBottom = 2
        BottomToTop = 3

    class BtnStyle(enum.Enum):
        """Enum for breadcrumb  button style options"""
        NoStyle = 1
        DefaultStyle = 2
        CustomStyle = 3

    itemClicked: ClassVar[Signal] = Signal(int, str)

    def __init__(self, items: List[Union[QWidget, str]], debug: bool = False, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.debug: bool = debug
        self.orientation = self.Orientation.HORIZONTAL
        self.readingDirection = self.ReadingDirection.LeftToRight
        self.btnStyle = self.BtnStyle.DefaultStyle
        self.btnCustomStyle: Optional[Any] = None
        self.separator: Union[str, QIcon] = ">"
        self.spacing: int = 1
        self.items: List[Union[QWidget, str]] = items
        self.layout: Optional[QLayout] = None
        self.loadUI()

    def setDebug(self, var: bool):
        if isinstance(var, bool):
            self.debug = var
        else:
            if self.debug:
                logging.warning(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {var} is not boolean.")

    def setBreadcrumbsOrientation(self, var: Union[int, 'QBreadcrumbs.Orientation']):
        if isinstance(var, int):
            self.orientation = self.Orientation(var)
        elif isinstance(var, self.Orientation):
            self.orientation = var
        else:
            if self.debug:
                logging.warning(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {var} is not int or QBreadcrumbs.Orientation.")
        
        self.loadUI()

    def setBtnStyle(self, var: Union[int, 'QBreadcrumbs.BtnStyle']):
        if isinstance(var, int):
            self.btnStyle = self.BtnStyle(var)
        elif isinstance(var, self.BtnStyle):
            self.btnStyle = var
        else:
            if self.debug:
                logging.warning(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {var} is not int or QBreadcrumbs.BtnStyle.")
        
        self._setupLayout()

    def setSeparator(self, var: Union[str, QIcon]):
        if isinstance(var, str) or isinstance(var, QIcon):
            self.separator = var
        else:
            if self.debug:
                logging.warning(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {var} is not str or QIcon.")
        
        self._setupLayout()

    def setSpacing(self, var: int):
        if isinstance(var, int):
            self.spacing = var
            if self.layout:
                self.layout.setSpacing(var)
        else:
            if self.debug:
                logging.warning(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {var} is not int.")

    def setItems(self, var: List[Union[QWidget, str]]):
        if isinstance(var, list):
            self.items = var
        else:
            if self.debug:
                logging.warning(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {var} is not list.")
        
        self._setupLayout()
                
    def setReadingDirection(self, var: Union[int, 'QBreadcrumbs.ReadingDirection']):
        if isinstance(var, int):
            self.readingDirection = self.ReadingDirection(var)
        elif isinstance(var, self.ReadingDirection):
            self.readingDirection = var
        else:
            if self.debug:
                logging.warning(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {var} is not int or QBreadcrumbs.ReadingDirection.")
        
        self.loadUI()

    def loadUI(self):
        if self.orientation == self.Orientation.HORIZONTAL:
            self.layout: QLayout = QHBoxLayout()
            if self.readingDirection == self.ReadingDirection.LeftToRight:
                self.layout.setDirection(QBoxLayout.Direction.LeftToRight)
            elif self.readingDirection == self.ReadingDirection.RightToLeft:
                self.layout.setDirection(QBoxLayout.Direction.RightToLeft)
            else:
                self.layout.setDirection(QBoxLayout.Direction.LeftToRight)
                if self.debug:
                    logging.warning(
                        f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {self.readingDirection} is not valid.")
                    sys.exit(1)

        elif self.orientation == self.Orientation.VERTICAL:
            self.layout: QLayout = QVBoxLayout()
            if self.readingDirection == QBreadcrumbs.ReadingDirection.TopToBottom:
                self.layout.setDirection(QBoxLayout.Direction.TopToBottom)
            elif self.readingDirection == QBreadcrumbs.ReadingDirection.BottomToTop:
                self.layout.setDirection(QBoxLayout.Direction.BottomToTop)
            else:
                self.layout.setDirection(QBoxLayout.Direction.TopToBottom)
                if self.debug:
                    logging.warning(
                        f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {self.readingDirection} is not valid.")
                    sys.exit(1)

        else:
            if self.debug:
                logging.warning(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {self.orientation} is not valid.")
                sys.exit(1)

        self.setLayout(self.layout)
        self.setAutoFillBackground(True)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(self.spacing)

        self._setupLayout()

    def _createBtn(self, text: str, index: int) -> QPushButton:
        btn = QPushButton(text)
        btn.setFlat(True)
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Réduire les marges
        btn.setContentsMargins(0, 0, 0, 0)
    
        # Calculer la taille basée sur le texte
        font_metrics = btn.fontMetrics()
        text_width = font_metrics.horizontalAdvance(text)
        text_height = font_metrics.height()
    
        # Ajouter une petite marge pour le confort visuel
        btn.setFixedSize(text_width + 10, text_height + 6)

        # Style du bouton
        if self.btnStyle == self.BtnStyle.NoStyle:
            btn.setStyleSheet("background-color: transparent;")

        elif self.btnStyle == self.BtnStyle.DefaultStyle:
            btn.setStyleSheet("background-color: transparent; color: blue;")

        elif self.btnStyle == self.BtnStyle.CustomStyle:
            btn.setStyleSheet(self.btnCustomStyle)
        else:
            btn.setStyleSheet("background-color: transparent; color: black;")
            if self.debug:
                logging.warning(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {self.btnStyle} is not valid.")

        btn.clicked.connect(lambda: self.itemClicked.emit(index, text))
        return btn
    
    def _setupLayout(self):
        """Set up the layout with current items."""
        self.cleanLayout()

        for i, a in enumerate(self.items):
            if isinstance(a, QWidget):
                self.layout.addWidget(a)
            elif isinstance(a, str):
                btn = self._createBtn(a, i)
                self.layout.addWidget(btn)

            if i < len(self.items) - 1:
                if isinstance(self.separator, str):
                    self.layout.addWidget(QLabel(self.separator))
                elif isinstance(self.separator, QIcon):
                    lbl = QLabel()
                    lbl.setPixmap(self.separator.pixmap(20, 20))
                    self.layout.addWidget(lbl)

        if self.debug:
            logging.info(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Breadcrumbs loaded successfully.")

    def cleanLayout(self):
        """Clear all items from the layout."""
        while self.layout.count():
            item = self.layout.takeAt(0)
            if widget := item.widget():
                widget.deleteLater()
        if self.debug:
            logging.debug("Cleared breadcrumb layout")


# class QBreadcrumbsv2(QWidget):
#     class Direction(enum.Enum):
#         HORIZONTAL = 'H'
#         VERTICAL = 'V'

#     itemClicked = Signal(int, str)

#     @typing.overload
#     def __init__(self, debug: bool, parent: Optional[QWidget] = None): ...

#     @typing.overload
#     def __init__(self, items: List[Union[QWidget, str]], parent: Optional[QWidget] = None): ...

#     @typing.overload
#     def __init__(self, items: List[Union[QWidget, str]], direction: Direction, parent: Optional[QWidget] = None): ...

#     @typing.overload
#     def __init__(self, items: List[Union[QWidget, str]], separator: Union[str, QIcon], parent: Optional[QWidget] = None): ...

#     @typing.overload
#     def __init__(self, items: List[Union[QWidget, str]], debug: bool, parent: Optional[QWidget] = None): ...

#     def __init__(
#         self,
#         options: Optional[Union[Direction, str, QIcon, bool, List[Union[QWidget, str]]]] = None,
#         parent: Optional[QWidget] = None
#     ):
#         """
#         Initialise QBreadcrumbs avec différentes configurations possibles.
        
#         Les différentes signatures possibles sont:
#         1. QBreadcrumbs(items, parent=None)
#         2. QBreadcrumbs(items, direction, parent=None)
#         3. QBreadcrumbs(items, separator, parent=None)
#         4. QBreadcrumbs(items, debug, parent=None)
#         5. QBreadcrumbs(debug, parent=None)
#         """
#         super().__init__(parent)
        
#         # Valeurs par défaut
#         self.items = ["Home", "Summary", "Details", "Edit", "Symbols"]
#         self.direction = self.Direction.HORIZONTAL
#         self.separator = ">"
#         self.debug = False

#         # Configuration selon les paramètres reçus
#         if options is not None:
#             if isinstance(options, list):
#                 self.setItems(options)
#             elif isinstance(options, self.Direction):
#                 self.setDirection(options)
#             elif isinstance(options, (str, QIcon)):
#                 self.setSeparator(options)
#             elif isinstance(options, bool):
#                 self.setDebug(options)

#         # Initialisation du layout
#         self.layout = QHBoxLayout() if self.direction == self.Direction.HORIZONTAL else QVBoxLayout()
#         self.layout.setSpacing(5)
#         self.layout.setContentsMargins(0, 0, 0, 0)
#         self.setLayout(self.layout)
        
#         # Création des éléments
#         self._create_items()

#     def _create_separator_label(self) -> QLabel:
#         """Crée un label pour le séparateur"""
#         label = QLabel()
#         if isinstance(self.separator, str):
#             label.setText(self.separator)
#         else:  # QIcon
#             label.setPixmap(self.separator.pixmap(20, 20))
#         return label

#     def _create_button(self, text: str, index: int) -> QPushButton:
#         """Crée un bouton pour un élément texte"""
#         btn = QPushButton(text)
#         btn.setFlat(True)
#         btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
#         btn.setStyleSheet("QPushButton { border: none; color: blue; }")
#         btn.clicked.connect(lambda _, idx=index, txt=text: self.itemClicked.emit(idx, txt))
#         return btn

#     def _create_items(self) -> None:
#         """Crée les éléments du fil d'Ariane"""
#         # Nettoyer le layout existant
#         while self.layout.count():
#             item = self.layout.takeAt(0)
#             if widget := item.widget():
#                 widget.deleteLater()

#         # Créer les nouveaux éléments
#         for i, item in enumerate(self.items):
#             # Ajouter l'élément (widget ou bouton)
#             if isinstance(item, QWidget):
#                 self.layout.addWidget(item)
#             else:  # str
#                 self.layout.addWidget(self._create_button(str(item), i))
            
#             # Ajouter le séparateur si ce n'est pas le dernier élément
#             if i < len(self.items) - 1:
#                 self.layout.addWidget(self._create_separator_label())

#     def setDebug(self, value: bool) -> None:
#         self.debug = value
    
#     def setItems(self, items: List[Union[QWidget, str]]) -> None:
#         self.items = items
#         self._create_items()
    
#     def setSeparator(self, separator: Union[str, QIcon]) -> None:
#         self.separator = separator
#         self._create_items()
    
#     def setDirection(self, direction: Direction) -> None:
#         new_layout = QHBoxLayout() if direction == self.Direction.HORIZONTAL else QVBoxLayout()
#         new_layout.setSpacing(5)
#         new_layout.setContentsMargins(0, 0, 0, 0)

