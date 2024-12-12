from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
import os
import logging

""" 
    Generator API: IntelliCode API Usage Examples
    
    Derived from 10 examples found on GitHub
    Title: Real World Examples of qtpy.QtWidgets.QAction.setStatusTip()
    Grouped by signature: setStatusTip(arg1)
"""
#  wkentaro/chainer-mask-rcnn/lib.py
def newAction(parent, text, slot=None, shortcut=None, icon=None,
              tip=None, checkable=False, enabled=True):
    """Create a new action and assign callbacks, shortcuts, etc."""
    a = QtWidgets.QAction(text, parent)
    if icon is not None:
        a.setIcon(newIcon(icon))
    if shortcut is not None:
        if isinstance(shortcut, (list, tuple)):
            a.setShortcuts(shortcut)
        else:
            a.setShortcut(shortcut)
    if tip is not None:
        a.setToolTip(tip)
        a.setStatusTip(tip)
    if slot is not None:
        a.triggered.connect(slot)
    if checkable:
        a.setCheckable(True)
    a.setEnabled(enabled)
    return a

#  wkentaro/labelme/qt.py
def newAction(
    parent,
    text,
    slot=None,
    shortcut=None,
    icon=None,
    tip=None,
    checkable=False,
    enabled=True,
    checked=False,
):
    """Create a new action and assign callbacks, shortcuts, etc."""
    a = QtWidgets.QAction(text, parent)
    if icon is not None:
        a.setIconText(text.replace(" ", "\n"))
        a.setIcon(newIcon(icon))
    if shortcut is not None:
        if isinstance(shortcut, (list, tuple)):
            a.setShortcuts(shortcut)
        else:
            a.setShortcut(shortcut)
    if tip is not None:
        a.setToolTip(tip)
        a.setStatusTip(tip)
    if slot is not None:
        a.triggered.connect(slot)
    if checkable:
        a.setCheckable(True)
    a.setEnabled(enabled)
    a.setChecked(checked)
    return a

# PaddleCV-SIG/EISeg/qt.py
def newAction(
    parent,
    text,
    slot=None,
    shortcutName=None,
    icon=None,
    tip=None,
    checkable=False,
    enabled=True,
    checked=False,
):
    """Create a new action and assign callbacks, shortcuts, etc."""
    a = QtWidgets.QAction(text, parent)
    a.setData(shortcutName)
    # a = QtWidgets.QAction("", parent)
    if icon is not None:
        a.setIconText(text.replace(" ", "\n"))
        a.setIcon(newIcon(icon))
    shortcut = shortcuts.get(shortcutName, None)
    if shortcut is not None:
        if isinstance(shortcut, (list, tuple)):
            a.setShortcuts(shortcut)
        else:
            a.setShortcut(shortcut)
    if tip is not None:
        a.setToolTip(tip)
        a.setStatusTip(tip)
    if slot is not None:
        a.triggered.connect(slot)
    if checkable:
        a.setCheckable(True)
    a.setEnabled(enabled)
    a.setChecked(checked)
    return a

#  PaddlePaddle/PaddleSeg/qt.py
def newAction(
        parent,
        text,
        slot=None,
        shortcutName=None,
        icon=None,
        tip=None,
        checkable=False,
        enabled=True,
        checked=False, ):
    """Create a new action and assign callbacks, shortcuts, etc."""
    a = QtWidgets.QAction(text, parent)
    a.setData(shortcutName)
    # a = QtWidgets.QAction("", parent)
    if icon is not None:
        a.setIconText(text.replace(" ", "\n"))
        a.setIcon(newIcon(icon))
    shortcut = shortcuts.get(shortcutName, None)
    if shortcut is not None:
        if isinstance(shortcut, (list, tuple)):
            a.setShortcuts(shortcut)
        else:
            a.setShortcut(shortcut)
    if tip is not None:
        a.setToolTip(tip)
        a.setStatusTip(tip)
    if slot is not None:
        a.triggered.connect(slot)
    if checkable:
        a.setCheckable(True)
    a.setEnabled(enabled)
    a.setChecked(checked)
    return a

#  gridsync/gridsync/model.py
def add_folder(self, path: str) -> None:
        basename = os.path.basename(os.path.normpath(path))
        if self.findItems(basename):
            logging.warning(
                "Tried to add a folder (%s) that already exists", basename
            )
            return
        composite_pixmap = CompositePixmap(self.icon_folder.pixmap(256, 256))
        name = QStandardItem(QIcon(composite_pixmap), basename)
        name.setToolTip(path)
        status = QStandardItem()
        mtime = QStandardItem()
        size = QStandardItem()
        action = QStandardItem()
        self.appendRow([name, status, mtime, size, action])
        action_bar = QToolBar()
        action_bar.setIconSize(QSize(16, 16))
        if sys.platform == "darwin":
            # See: https://bugreports.qt.io/browse/QTBUG-12717
            action_bar.setStyleSheet(
                "background-color: {0}; border: 0px {0}".format(
                    self.view.palette().base().color().name()
                )
            )
        action_bar_action = QAction(self.icon_action, "Action...", self)
        action_bar_action.setStatusTip("Action...")
        action_bar_action.triggered.connect(self.view.on_right_click)
        action_bar.addAction(action_bar_action)
        self.view.setIndexWidget(action.index(), action_bar)
        self.view.hide_drop_label()
        self.set_status(basename, MagicFolderStatus.LOADING)
    
# royerlab/aydin/gui.py
def setupMenubar(self):
        """Method to populate menubar."""

        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu(' &File')
        runMenu = mainMenu.addMenu(' &Run')
        preferencesMenu = mainMenu.addMenu(' &Preferences')
        helpMenu = mainMenu.addMenu(' &Help')

        # File Menu
        startPageButton = QAction('Add File(s)', self)
        startPageButton.setStatusTip('Add new files')
        startPageButton.triggered.connect(
            self.main_widget.tabs["File(s)"].openFileNamesDialog
        )
        fileMenu.addAction(startPageButton)

        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # Run Menu
        startButton = QAction('Start', self)
        startButton.setStatusTip('Start denoising')
        startButton.triggered.connect(
            self.main_widget.processing_job_runner.prep_and_run
        )
        runMenu.addAction(startButton)

        saveOptionsJSONButton = QAction('Save Options JSON', self)
        saveOptionsJSONButton.setStatusTip('Save options JSON')
        saveOptionsJSONButton.triggered.connect(
            lambda: self.main_widget.save_options_json()
        )
        runMenu.addAction(saveOptionsJSONButton)

        loadPretrainedModelButton = QAction('Load Pretrained Model', self)
        loadPretrainedModelButton.setStatusTip('Load Pretrained Model')
        loadPretrainedModelButton.triggered.connect(
            lambda: self.main_widget.load_pretrained_model()
        )
        runMenu.addAction(loadPretrainedModelButton)

        # Preferences Menu
        self.basicModeButton = QAction('Basic mode', self)
        self.basicModeButton.setEnabled(False)
        self.basicModeButton.setStatusTip('Switch to basic mode')
        self.basicModeButton.triggered.connect(
            lambda: self.main_widget.toggle_basic_advanced_mode()
        )
        preferencesMenu.addAction(self.basicModeButton)

        self.advancedModeButton = QAction('Advanced mode', self)
        self.advancedModeButton.setStatusTip('Switch to advanced mode')
        self.advancedModeButton.triggered.connect(
            lambda: self.main_widget.toggle_basic_advanced_mode()
        )
        preferencesMenu.addAction(self.advancedModeButton)

        # Help Menu
        versionButton = QAction("ver" + self.version, self)
        helpMenu.addAction(versionButton)