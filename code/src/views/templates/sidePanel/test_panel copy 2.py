#! usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import sys
from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
import qtawesome as qta


def main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()

    warning_icon = QApplication.style().standardIcon(QStyle.SP_MessageBoxWarning)
    critical_icon = QApplication.style().standardIcon(QStyle.SP_MessageBoxCritical)
    cog_icon = qta.icon("fa5s.cog")

    dock_1 = QDockWidget("warning", main_window)
    dock_1.setWindowIcon(cog_icon)

    dock_2 = QDockWidget("critical", main_window)
    dock_2.setWindowIcon(critical_icon)

    main_window.addDockWidget(Qt.LeftDockWidgetArea, dock_1)
    main_window.addDockWidget(Qt.RightDockWidgetArea, dock_2)

    def onLocationChanged(area):
        icon_dict = {}
        for _dock in main_window.findChildren(QDockWidget):
            icon_dict[_dock.windowTitle()] = _dock.windowIcon()

        for tab_bar in main_window.findChildren(QTabBar):
            for idx in range(tab_bar.count()):
                if tab_bar.tabText(idx) in icon_dict:
                    tab_bar.setTabIcon(idx, icon_dict[tab_bar.tabText(idx)])

    for dock in main_window.findChildren(QDockWidget):
        dock.dockLocationChanged.connect(onLocationChanged)
    onLocationChanged(0)

    # afficher la version de qt utilisée
    print("Qt version:", PYQT_VERSION_STR)
    main_window.show()
    app.exec_()


if __name__ == "__main__":
    main()