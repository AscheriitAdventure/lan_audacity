from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import logging
import inspect

from .tab import Tab


class WelcomeTab(Tab):
    """Welcome tab shown by default when the application starts"""

    def __init__(self, parent=None):
        super().__init__(parent, Tab.TabType.DEFAULT, "Welcome")
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(2)
        main_layout.setContentsMargins(2, 2, 2, 2)

        # Add QScrollArea as main container
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Create container widget for scroll area
        container = QWidget()
        scroll_layout = QVBoxLayout(container)
        scroll_layout.setSpacing(2)
        scroll_layout.setContentsMargins(0, 0, 0, 0)

        # Add scroll area to main layout
        main_layout.addWidget(scroll)
        scroll.setWidget(container)

        # Use scroll_layout instead of main_layout for content
        main_layout = scroll_layout

        # Header section
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)

        title = QLabel("Welcome to LAN Audacity")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Get started with your network management")
        subtitle.setStyleSheet("font-size: 16px; color: #666;")

        header_layout.addWidget(title, alignment=Qt.AlignCenter)
        header_layout.addWidget(subtitle, alignment=Qt.AlignCenter)

        # Actions section
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setSpacing(20)

        # Start box
        start_box = self._create_action_box(
            "Get Started",
            [
                ("New Project", "mdi6.folder-plus-outline", "new_project"),
                ("Open Project", "mdi6.folder-open-outline", "open_folder_project"),
                ("Import Project", "mdi6.folder-download-outline", None)
            ]
        )

        # Recent box
        recent_box = self._create_action_box(
            "Recent Projects",
            [("No recent projects", "", None)],
            fixed_height=200
        )

        # Help box
        help_box = self._create_action_box(
            "Help & Resources",
            [
                ("Documentation", "mdi6.book-open-page-variant-outline", None),
                ("Tutorial", "mdi6.school-outline", None),
                ("About", "mdi6.information-outline", None)
            ]
        )

        actions_layout.addWidget(start_box)
        actions_layout.addWidget(recent_box)
        actions_layout.addWidget(help_box)

        # Add all sections to main layout
        main_layout.addWidget(header_widget)
        main_layout.addWidget(actions_widget)
        main_layout.addStretch()

    def _create_action_box(self, title: str, actions: list, fixed_height: int = None) -> QGroupBox:
        """Create a grouped box of actions

        Args:
            title (str): Box title
            actions (list): List of tuples (label, icon_name, callback_name)
            fixed_height (int, optional): Fixed height for the box
        """
        box = QGroupBox(title)
        box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ccc;
                border-radius: 6px;
                margin-top: 1em;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)

        if fixed_height:
            box.setFixedHeight(fixed_height)

        layout = QVBoxLayout(box)
        layout.setSpacing(10)

        for label, icon_name, callback_name in actions:
            btn = QPushButton(label)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 8px;
                    border: none;
                    background: transparent;
                }
                QPushButton:hover {
                    background: #f0f0f0;
                    border-radius: 4px;
                }
            """)

            if icon_name:
                from qtawesome import icon
                btn.setIcon(icon(icon_name))

            if callback_name and hasattr(self.parent(), callback_name):
                btn.clicked.connect(getattr(self.parent(), callback_name))
            elif not callback_name:
                btn.setEnabled(False)

            layout.addWidget(btn)

        layout.addStretch()
        return box

    def update_recent_projects(self, recent_projects: list) -> None:
        """Update the recent projects list

        Args:
            recent_projects (list): List of recent project objects
        """
        recent_box = self.findChild(QGroupBox, "Recent Projects")
        if recent_box:
            # Clear existing buttons
            while recent_box.layout().count() > 0:
                item = recent_box.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            # Add new project buttons
            if recent_projects:
                for project in recent_projects:
                    btn = QPushButton(project.name)
                    btn.setStyleSheet("""
                        QPushButton {
                            text-align: left;
                            padding: 8px;
                            border: none;
                            background: transparent;
                        }
                        QPushButton:hover {
                            background: #f0f0f0;
                            border-radius: 4px;
                        }
                    """)
                    btn.clicked.connect(
                        lambda checked, p=project: self.parent().open_recent_project(p)
                    )
                    recent_box.layout().addWidget(btn)
            else:
                label = QLabel("No recent projects")
                label.setStyleSheet("color: #666; padding: 8px;")
                recent_box.layout().addWidget(label)

            recent_box.layout().addStretch()

