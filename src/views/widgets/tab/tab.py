from enum import Enum, auto
from qtpy.QtWidgets import QWidget

class Tab(QWidget):
    class TabType(Enum):
        DEFAULT = auto()
        EDITOR = auto()
        NETWORK = auto()
        EXTENSION = auto()

    """Base class for all tabs"""

    def __init__(self, parent=None, tab_type: TabType = None, title: str = ""):
        super().__init__(parent)
        self.tab_type = tab_type
        self.title = title
        self.modified = False
        self.debug: bool = False

    def get_title(self) -> str:
        return f"{'*' if self.modified else ''}{self.title}"
