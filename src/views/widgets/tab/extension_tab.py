from .tab import Tab
from typing import Dict, Any
from qtpy.QtWidgets import QVBoxLayout, QLabel


class ExtensionTab(Tab):
    """Tab for extensions/plugins"""

    def __init__(self, parent=None, extension_data: Dict[str, Any] = None):
        title = extension_data.get('name', 'Extension')
        super().__init__(parent, Tab.TabType.EXTENSION, title)
        self.extension_data = extension_data
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        # Add extension specific widgets here
        # This is a placeholder for the actual implementation
        layout.addWidget(QLabel(f"Extension: {self.title}"))
