from typing import List
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import logging
import inspect

from .tab import Tab


class TabManager(QTabWidget):
    """Enhanced tab widget with additional management features"""

    tab_closed = Signal(Tab)  # Emitted when a tab is closed
    tab_changed = Signal(Tab)  # Emitted when active tab changes

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)

        # Connect signals
        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.on_current_changed)

    def add_tab(self, tab: Tab) -> int:
        """Add a new tab and return its index"""
        index = self.addTab(tab, tab.get_title())
        return index

    def close_tab(self, index: int) -> None:
        """Handle tab closing with confirmation if needed"""
        tab = self.widget(index)
        if isinstance(tab, Tab):
            if tab.modified:
                reply = QMessageBox.question(
                    self,
                    'Save Changes?',
                    f'Do you want to save changes to {tab.title}?',
                    QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel
                )

                if reply == QMessageBox.StandardButton.Save:
                    # Handle saving
                    pass
                elif reply == QMessageBox.StandardButton.Cancel:
                    return

            self.removeTab(index)
            self.tab_closed.emit(tab)

    def update_tab_title(self, tab: Tab) -> None:
        """Update the title of a tab"""
        index = self.indexOf(tab)
        if index >= 0:
            self.setTabText(index, tab.get_title())

    def on_current_changed(self, index: int) -> None:
        """Handle tab selection change"""
        if index >= 0:
            tab = self.widget(index)
            if isinstance(tab, Tab):
                self.tab_changed.emit(tab)

    def get_tabs_by_type(self, tab_type: Tab.TabType) -> List[Tab]:
        """Get all tabs of a specific type"""
        return [
            self.widget(i) for i in range(self.count())
            if isinstance(self.widget(i), Tab) and self.widget(i).tab_type == tab_type
        ]

