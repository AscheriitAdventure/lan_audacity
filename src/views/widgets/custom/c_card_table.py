from typing import *
import logging
import inspect
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
from datetime import datetime
import qtawesome as qta
import json
import pandas as pd
import xml.dom.minidom as md
from xml.etree import ElementTree as ET

from src.views.widgets import *
from .c_table_filter import CustomTableFilter as CTF


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
        
        logging.info(f"Initializing CustomCardTable with title: {title}, keys: {key_table}, data: {data_table}")
        # Initialize the title of the card
        self.headerPanel: TitleWithActions = TitleWithActions(title=title, debug=self.debug, parent=self)
        self.setPositionCard("top", self.headerPanel)
        # Initialize the table environment
        logging.debug(f"Initializing table with keys: {key_table}")
        try:
            self.initTable(key_table)
        except Exception as e:
            logging.error(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error during table initialization: {str(e)}")
    
        if data_table is not None and len(data_table) > 0:
            try:
                self.loadData(data_table)
            except Exception as e:
                logging.error(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error during data loading: {str(e)}")

    def initTable(self, key_table: Union[Tuple[str], List[str]]) -> None:
        """Initialize the table."""
        self.cct = QTableWidget(self.parent())
        self.cct.setColumnCount(len(key_table))

        for i, key in enumerate(key_table):
            self.cct.setColumnWidth(i, 50)

        self.cct.setRowCount(0)
        self.cct.setHorizontalHeaderLabels(key_table)
        self.cct.resizeColumnsToContents()
        self.cct.resizeRowsToContents()
        self.cct.setSortingEnabled(True)
        self.cct.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.cct.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.cct.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.setPositionCard("center", self.cct)
    
    def togglePositionPanel(self, pos: str, is_visible: bool) -> None:
        """
        Toggle the visibility of a panel at a specific position.
    
        Args:
            pos: Position of the panel ("top", "right", "bottom", "left")
            is_visible: True to show the panel, False to hide it
        """
        if pos not in ["top", "right", "bottom", "left"]:
            logging.error(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Invalid position '{pos}'. Expected one of ['top', 'right', 'bottom', 'left'].")
            return
        
        index = self._findSectionIndex(pos)
        if index != -1:
            # Met à jour le paramètre is_visible dans la configuration
            self.sections[index]["is_visible"] = is_visible
        
            # Récupère le widget et met à jour sa visibilité
            widget = self.getPositionWidget(pos)
            if widget:
                widget.setVisible(is_visible)
            
            # Marque la section comme nécessitant une mise à jour
            self.markSectionDirty(pos)
        
            # Optionnellement, vous pourriez vouloir réorganiser les widgets
            self._arrangeWidgets()
            self.update()
        else:
            logging.warning(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: No section found with position '{pos}'")

    #### Filter Right Panel ####
    def initRightPanel(self) -> None:
        """Initialize the right panel with the CustomTableFilter."""
        # Créer le widget de filtrage
        # Créer l'instance de CustomTableFilter en lui passant le tableau
        self.filter = CTF(self.cct, debug=self.debug, parent=self)
    
        # Configurer le panneau droit avec notre filtre
        self.crp = self.filter
    
        # Par défaut, cacher le panneau de filtre
        self.sections[self._findSectionIndex("right")]["is_visible"] = False
    
        # Attacher le panneau au conteneur
        self.setPositionCard("right", self.crp)
    
        # Connecter le signal de changement de filtre à une méthode de mise à jour si nécessaire
        self.filter.filterChanged.connect(self.onFilterChanged)

    def onFilterChanged(self) -> None:
        """Appelé lorsque les filtres sont modifiés."""
        # Cette méthode peut être utilisée pour effectuer des actions supplémentaires
        # lorsque les filtres changent, comme mettre à jour des statistiques, etc.
        logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Filters changed")

    def loadData(self, data_table: Any) -> None:
        """Load the data into the table."""
        if not isinstance(data_table, (list, tuple)):
            logging.error(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Invalid data type: {type(data_table)}. Expected list or tuple.")
            return
    
        # Effacer le tableau existant
        self.cct.setRowCount(0)
    
        for i, row in enumerate(data_table):
            self.cct.insertRow(i)
            for j, item in enumerate(row):
                self.cct.setItem(i, j, QTableWidgetItem(str(item)))
    
        # Mettre à jour les widgets de filtrage s'ils existent
        if hasattr(self, 'filter') and self.filter is not None:
            self.filter.updateFilterWidgets()

    #### setter methods ####
    def setFilterPanel(self, var: bool) -> None:
        """add Toggle Right Panel Btn to  to Title with Actions."""
        self.toggleRightPanelBtn = QPushButton(self)
        self.toggleRightPanelBtn.setIcon(qta.icon("mdi6.filter-settings")) # "mdi6.filter-settings", "mdi6.filter-cog"
        self.toggleRightPanelBtn.setToolTip("Afficher/Masquer le panneau de filtre")
        self.toggleRightPanelBtn.setFlat(True)

        self.toggleRightPanelBtn.clicked.connect(lambda: self.togglePositionPanel("right", not self.sections[self._findSectionIndex("right")]["is_visible"]))

        self.headerPanel.addBtnAction(self.toggleRightPanelBtn)
        # update the title widget with the new button
        
        self.initRightPanel()

    def setExportBtn(self, var: bool) -> None:
        """Ajouter un bouton d'exportation au panneau de titre avec un menu déroulant.

        Args:
            var: True pour activer, False pour désactiver
        """
        if not var:
            return
        
        # Créer le bouton d'exportation
        self.exportBtn = QPushButton(self)
        self.exportBtn.setIcon(qta.icon("fa5s.file-export", color="Navy"))
        self.exportBtn.setToolTip("Exporter les données")
        self.exportBtn.setFlat(True)
    
        # Créer le menu d'exportation
        self.exportMenu = QMenu(self)
    
        # Ajouter les actions d'exportation
        self.exportCsvAction = QAction(qta.icon("mdi6.file-delimited", color="OliveDrab"), "Exporter en CSV", self)
        self.exportCsvAction.triggered.connect(self.exportToCsv)
        self.exportMenu.addAction(self.exportCsvAction)
    
        self.exportExcelAction = QAction(qta.icon("mdi6.file-excel", color="ForestGreen"), "Exporter en Excel", self)
        self.exportExcelAction.triggered.connect(self.exportToExcel)
        self.exportMenu.addAction(self.exportExcelAction)
    
        self.exportJsonAction = QAction(qta.icon("mdi6.file-code", color="Orange"), "Exporter en JSON", self)
        self.exportJsonAction.triggered.connect(self.exportToJson)
        self.exportMenu.addAction(self.exportJsonAction)
        
        self.exportXmlAction = QAction(qta.icon("mdi6.file-xml-box", color="FireBrick"), "Exporter en XML", self)
        self.exportXmlAction.triggered.connect(self.exportToXml)
        self.exportMenu.addAction(self.exportXmlAction)
    
        # Associer le menu au bouton
        self.exportBtn.setMenu(self.exportMenu)
    
        # Ajouter le bouton au panneau de titre
        self.headerPanel.addBtnAction(self.exportBtn)
        
    #### Export File Methods  (CSV, XLS, JSON, XML, etc...) ####

    def exportToCsv(self) -> None:
        """Exporter les données du tableau au format CSV."""
        dfl_n = self.generateExportFilename("csv")
        logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Export filename: {dfl_n}")

        try:
            # Demander le nom du fichier
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exporter en CSV", dfl_n, "Fichiers CSV (*.csv);;Tous les fichiers (*)")
        
            if not file_path:
                return  # L'utilisateur a annulé
            
            # Ajouter l'extension .csv si nécessaire
            if not file_path.lower().endswith('.csv'):
                file_path += '.csv'
            
            # Ouvrir le fichier en écriture
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                # Écrire les en-têtes
                headers:list = list()
                for col in range(self.cct.columnCount()):
                    if not self.cct.isColumnHidden(col):
                        header_item = self.cct.horizontalHeaderItem(col)
                        headers.append(header_item.text() if header_item else f"Column {col+1}")
            
                file.write(','.join([f'"{h}"' for h in headers]) + '\n')

                # Écrire les données
                for row in range(self.cct.rowCount()):
                    if not self.cct.isRowHidden(row):
                        row_data:list = list()
                        for col in range(self.cct.columnCount()):
                            if not self.cct.isColumnHidden(col):
                                item = self.cct.item(row, col)
                                text = item.text() if item else ""
                                # Échapper les guillemets et entourer de guillemets
                                row_data.append(f'"{text.replace('"', '""')}"')
                        file.write(','.join(row_data) + '\n')
                    
            logging.info(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Exported to CSV: {file_path}")
            QMessageBox.information(self, "Export réussi", f"Les données ont été exportées avec succès dans {file_path}")
            
        except Exception as e:
            logging.error(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error during CSV export: {str(e)}")
            QMessageBox.critical(self, "Erreur d'exportation", f"Une erreur s'est produite lors de l'exportation CSV:\n{str(e)}")

    def exportToExcel(self) -> None:
        """Exporter les données du tableau au format Excel."""
        dfl_n = self.generateExportFilename("xlsx")
        logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Export filename: {dfl_n}")
        try:            
            # Demander le nom du fichier
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exporter en Excel", dfl_n, "Fichiers Excel (*.xlsx);;Tous les fichiers (*)")
        
            if not file_path:
                return  # L'utilisateur a annulé
            
            # Ajouter l'extension .xlsx si nécessaire
            if not file_path.lower().endswith('.xlsx'):
                file_path += '.xlsx'
            
            # Collecter les données
            data:dict = dict()
            headers:list = list()
        
            for col in range(self.cct.columnCount()):
                if not self.cct.isColumnHidden(col):
                    header_item = self.cct.horizontalHeaderItem(col)
                    header = header_item.text() if header_item else f"Column {col+1}"
                    headers.append(header)
                    column_data:list = list()
                
                    for row in range(self.cct.rowCount()):
                        if not self.cct.isRowHidden(row):
                            item = self.cct.item(row, col)
                            column_data.append(item.text() if item else "")
                
                    data[header] = column_data
                
            # Créer un DataFrame pandas
            df = pd.DataFrame(data)
        
            # Exporter vers Excel
            df.to_excel(file_path, index=False, engine='xlsxwriter')
        
            logging.info(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Exported to Excel: {file_path}")
            QMessageBox.information(self, "Export réussi", f"Les données ont été exportées avec succès dans {file_path}")
            
        except Exception as e:
            logging.error(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error during Excel export: {str(e)}")
            QMessageBox.critical(self, "Erreur d'exportation", f"Une erreur s'est produite lors de l'exportation Excel:\n{str(e)}")

    def exportToJson(self) -> None:
        """Exporter les données du tableau au format JSON."""
        dfl_n = self.generateExportFilename("json")
        logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Export filename: {dfl_n}")
        try:        
            # Demander le nom du fichier
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exporter en JSON", dfl_n, "Fichiers JSON (*.json);;Tous les fichiers (*)")
        
            if not file_path:
                return  # L'utilisateur a annulé
            
            # Ajouter l'extension .json si nécessaire
            if not file_path.lower().endswith('.json'):
                file_path += '.json'
            
            # Collecter les données
            data:list = list()
            headers:list = list()
        
            for col in range(self.cct.columnCount()):
                if not self.cct.isColumnHidden(col):
                    header_item = self.cct.horizontalHeaderItem(col)
                    headers.append(header_item.text() if header_item else f"Column {col+1}")
        
            for row in range(self.cct.rowCount()):
                if not self.cct.isRowHidden(row):
                    row_data:dict = dict()
                    for col in range(self.cct.columnCount()):
                        if not self.cct.isColumnHidden(col):
                            header = headers[col - (headers.index(headers[col]) - col)]
                            item = self.cct.item(row, col)
                            row_data[header] = item.text() if item else ""
                    data.append(row_data)
                
            # Écrire les données JSON
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            
            logging.info(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Exported to JSON: {file_path}")
            QMessageBox.information(self, "Export réussi", f"Les données ont été exportées avec succès dans {file_path}")
            
        except Exception as e:
            logging.error(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error during JSON export: {str(e)}")
            QMessageBox.critical(self, "Erreur d'exportation", f"Une erreur s'est produite lors de l'exportation JSON:\n{str(e)}")

    def exportToXml(self) -> None:
        """Exporter les données du tableau au format XML."""
        try:
            # Générer le nom de fichier par défaut
            default_filename = self.generateExportFilename("xml")
            logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Export filename: {default_filename}")
        
            # Demander le nom du fichier, avec le nom par défaut prérempli
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exporter en XML", default_filename, "Fichiers XML (*.xml);;Tous les fichiers (*)")
        
            if not file_path:
                return  # L'utilisateur a annulé
            
            # Ajouter l'extension .xml si nécessaire
            if not file_path.lower().endswith('.xml'):
                file_path += '.xml'
            
            # Créer l'élément racine
            root = ET.Element("data")
            root.set("table", self.getTableName())
            root.set("generated", datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
        
            # Récupérer les en-têtes
            headers = []
            for col in range(self.cct.columnCount()):
                if not self.cct.isColumnHidden(col):
                    header_item = self.cct.horizontalHeaderItem(col)
                    headers.append(header_item.text() if header_item else f"Column{col+1}")
        
            # Ajouter des métadonnées
            metadata = ET.SubElement(root, "metadata")
            columns_meta = ET.SubElement(metadata, "columns")
        
            for header in headers:
                column = ET.SubElement(columns_meta, "column")
                column.set("name", header)
        
            # Ajouter les données
            rows_element = ET.SubElement(root, "rows")
        
            for row in range(self.cct.rowCount()):
                if not self.cct.isRowHidden(row):
                    row_element = ET.SubElement(rows_element, "row")
                    row_element.set("id", str(row))
                
                    for col, header_index in enumerate([i for i in range(self.cct.columnCount()) if not self.cct.isColumnHidden(i)]):
                        column_name = headers[col]
                        # Remplacer les espaces par des underscores pour les noms d'éléments XML valides
                        safe_column_name = column_name.replace(" ", "_").replace(".", "_").replace(",", "_")
                    
                        # S'assurer que le nom commence par une lettre ou un underscore
                        if not (safe_column_name[0].isalpha() or safe_column_name[0] == '_'):
                            safe_column_name = "col_" + safe_column_name

                        cell_element = ET.SubElement(row_element, safe_column_name)
                        item = self.cct.item(row, header_index)
                        cell_element.text = item.text() if item else ""
        
            # Formatter le XML avec des retours à la ligne et des indentations
            xml_str = ET.tostring(root, encoding="utf-8")
            dom = md.parseString(xml_str)
            pretty_xml = dom.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")
        
            # Écrire dans le fichier
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(pretty_xml)
            
            logging.info(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Exported to XML: {file_path}")
            QMessageBox.information(self, "Export réussi", f"Les données ont été exportées avec succès dans {file_path}")
            
        except Exception as e:
            logging.error(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error during XML export: {str(e)}")
            QMessageBox.critical(self, "Erreur d'exportation", f"Une erreur s'est produite lors de l'exportation XML:\n{str(e)}")

    # Méthode auxiliaire pour obtenir les données du tableau (utilisée par les méthodes d'exportation)
    def getTableData(self) -> Tuple[List[str], List[List[str]]]:
        """
        Récupère les données du tableau sous forme de listes.
    
        Returns:
            Tuple contenant (en-têtes, données)
        """
        headers:list = list()
        for col in range(self.cct.columnCount()):
            if not self.cct.isColumnHidden(col):
                header_item = self.cct.horizontalHeaderItem(col)
                headers.append(header_item.text() if header_item else f"Column {col+1}")
    
        data:list = list()
        for row in range(self.cct.rowCount()):
            if not self.cct.isRowHidden(row):
                row_data:list = list()
                for col in range(self.cct.columnCount()):
                    if not self.cct.isColumnHidden(col):
                        item = self.cct.item(row, col)
                        row_data.append(item.text() if item else "")
                data.append(row_data)
    
        return headers, data

    def generateExportFilename(self, extension: str) -> str:
        """
        Génère un nom de fichier formaté pour l'exportation.
    
        Format: <AAAAMMJJ>_<HH:MM:SS>_<nom du réseau>_<nom du tableau extrait>.<extension>

        Args:
            extension: Extension du fichier sans le point (ex: "csv", "xlsx", "json")
    
        Returns:
            Nom de fichier formaté
        """
    
        # Date et heure actuelles
        now = datetime.now()
    
        # Construire le nom de fichier
        filename = f"{now.strftime("%Y%m%d_%H%M%S")}_{self.getTabName()}_{self.getTableName()}.{extension}"
    
        # Remplacer les caractères problématiques
        filename = filename.replace(":", "-").replace(" ", "_")
    
        return filename
    
    def getTabName(self) -> str:
        """
        Récupère le nom de l'objet parent.
        """
        logging.info(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: parent 0: {self.parent()}")
        return "networkTab"

    def getTableName(self) -> str:
        """
        Récupère le nom du tableau extrait.
        """
        # Par défaut, utiliser le titre du Card
        return self.headerPanel.getTitle().replace(" ", "_").lower()
    
    #### Other methods ####
    