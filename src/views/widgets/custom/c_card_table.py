from typing import *
import logging
import inspect
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *

from src.views.widgets import *


class CustomCardTable(Card):
    def __init__(
            self, 
            title: str = "Custom Card Table",
            key_table: Union[Tuple[str], List[str]] = ["col1", "col2"],
            data_table: Optional[Any] = None,
            debug: Optional[bool] = False, 
            parent=None
        ) -> None:
        super(CustomCardTable, self).__init__(debug, parent)

        self.refreshBtn = QPushButton("RT")
        self.refreshBtn.setToolTip("Refresh the table")
        self.refreshBtn.setFlat(True)

        self.stopRefreshBtn = QPushButton("SR")
        self.stopRefreshBtn.setToolTip("Stop the refresh")
        self.stopRefreshBtn.setFlat(True)

        # Initialize the title of the card
        self.initTitle(title)
        # Initialize the table environment
        self.initTable(key_table)
        
        if data_table is not None and len(data_table) > 0:
            self.loadData(data_table)

    def initTitle(self, title: str) -> None:
        """Initialize the title of the card."""
        btn_ls = [self.refreshBtn]
        ttl_w = TitleWithActions(title, btn_ls, self.debug, self.parent())
        self.setPositionCard("top", ttl_w)

    def initTable(self, key_table: Union[Tuple[str], List[str]]) -> None:
        """Initialize the table."""
        self.cct = QTableWidget(self.parent())
        self.cct.setColumnCount(len(key_table))

        for i in enumerate(key_table):
            self.cct.setColumnWidth(i, 50)

        self.cct.setRowCount(0)
        self.cct.setHorizontalHeaderLabels(key_table)
        self.cct.setVerticalHeaderLabels([])
        self.cct.resizeColumnsToContents()
        self.cct.resizeRowsToContents()
        self.cct.setSortingEnabled(True)
        self.cct.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.cct.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.cct.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.setPositionCard("center", self.cct)

    def loadData(self, data_table: Any) -> None:
        """Load the data into the table."""
        if not isinstance(data_table, (list, tuple)):
            logging.error(f"Invalid data type: {type(data_table)}. Expected list or tuple.")
            return
        
        for i, row in enumerate(data_table):
            self.cct.insertRow(i)
            for j, item in enumerate(row):
                self.cct.setItem(i, j, QTableWidgetItem(str(item)))
    
    # reloadData: permet de recharger les données dans le tableau
    # stopRefresh: permet d'arrêter le rafraîchissement du tableau
    