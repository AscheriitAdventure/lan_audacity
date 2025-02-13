import typing
import enum
from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
import logging
import inspect
import sys


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
        NoStyle = 0
        DefaultStyle = 1
        CustomStyle = 2

    itemClicked: typing.ClassVar[Signal] = Signal(int, str)

    def __init__(self, items: typing.List[typing.Union[QWidget, str]], debug: bool = False, parent: typing.Optional[QWidget] = None):
        super().__init__(parent)
        self.debug: bool = debug
        self.orientation: QBreadcrumbs.Orientation = QBreadcrumbs.Orientation.HORIZONTAL
        self.readingDirection: QBreadcrumbs.ReadingDirection = QBreadcrumbs.ReadingDirection.LeftToRight
        self.btnStyle: QBreadcrumbs.BtnStyle = QBreadcrumbs.BtnStyle.DefaultStyle
        self.btnCustomStyle: typing.Optional[typing.Any] = None
        self.separator: typing.Union[str, QIcon] = ">"
        self.spacing: int = 1
        self.items: typing.List[typing.Union[QWidget, str]] = items
        self.loadUI()

    def setDebug(self, var: bool):
        if isinstance(var, bool):
            self.debug = var
        else:
            if self.debug:
                logging.warning(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {var} is not boolean.")

    # type: ignore
    def setBreadcrumbsOrientation(self, var: typing.Union[int, 'QBreadcrumbs.Orientation']):
        if isinstance(var, int):
            self.orientation = QBreadcrumbs.Orientation(var)
        elif isinstance(var, QBreadcrumbs.Orientation):
            self.orientation = var
        else:
            if self.debug:
                logging.warning(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {var} is not int or QBreadcrumbs.Orientation.")

    # type: ignore
    def setBtnStyle(self, var: typing.Union[int, 'QBreadcrumbs.BtnStyle']):
        if isinstance(var, int):
            self.btnStyle = QBreadcrumbs.BtnStyle(var)
        elif isinstance(var, QBreadcrumbs.BtnStyle):
            self.btnStyle = var
        else:
            if self.debug:
                logging.warning(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {var} is not int or QBreadcrumbs.BtnStyle.")

    def setSeparator(self, var: typing.Union[str, QIcon]):
        if isinstance(var, str) or isinstance(var, QIcon):
            self.separator = var
        else:
            if self.debug:
                logging.warning(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {var} is not str or QIcon.")

    def setSpacing(self, var: int):
        if isinstance(var, int):
            self.spacing = var
        else:
            if self.debug:
                logging.warning(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {var} is not int.")

    def setItems(self, var: typing.List[typing.Union[QWidget, str]]):
        if isinstance(var, list):
            self.items = var
        else:
            if self.debug:
                logging.warning(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {var} is not list.")

    # type: ignore
    def setReadingDirection(self, var: typing.Union[int, 'QBreadcrumbs.ReadingDirection']):
        if isinstance(var, int):
            self.readingDirection = QBreadcrumbs.ReadingDirection(var)
        elif isinstance(var, QBreadcrumbs.ReadingDirection):
            self.readingDirection = var
        else:
            if self.debug:
                logging.warning(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {var} is not int or QBreadcrumbs.ReadingDirection.")

    def loadUI(self):
        if self.orientation == QBreadcrumbs.Orientation.HORIZONTAL:
            self.layout: QLayout = QHBoxLayout()
            if self.readingDirection == QBreadcrumbs.ReadingDirection.LeftToRight:
                self.layout.setDirection(QBoxLayout.Direction.LeftToRight)
            elif self.readingDirection == QBreadcrumbs.ReadingDirection.RightToLeft:
                self.layout.setDirection(QBoxLayout.Direction.RightToLeft)
            else:
                self.layout.setDirection(QBoxLayout.Direction.LeftToRight)
                if self.debug:
                    logging.warning(
                        f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error value {self.readingDirection} is not valid.")
                    sys.exit(1)

        elif self.orientation == QBreadcrumbs.Orientation.VERTICAL:
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
        
        self.update()

    def _createBtn(self, text: str, index: int) -> QPushButton:
        btn = QPushButton(text)
        btn.setFlat(True)
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        if self.btnStyle == QBreadcrumbs.BtnStyle.NoStyle:
            btn.setStyleSheet("background-color: transparent;")

        elif self.btnStyle == QBreadcrumbs.BtnStyle.DefaultStyle:
            btn.setStyleSheet("background-color: transparent; color: blue;")

        elif self.btnStyle == QBreadcrumbs.BtnStyle.CustomStyle:
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
                self.layout.addWidget(QLabel(self.separator))

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
