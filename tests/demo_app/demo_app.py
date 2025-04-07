from qtpy.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from src.models import Interfaces
from src.views.widgets import Card as CardFrame
from qtpy.QtWidgets import QLabel, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from qtpy.QtCore import Qt
from typing import Any, Dict, List, Tuple, Union
import inspect

def object_to_cardframe(obj: Any, parent=None, title=None) -> QWidget:
    """
    Convertit un objet Python en CardFrame.
    
    Args:
        obj: L'objet à convertir
        parent: Le widget parent
        title: Titre optionnel pour la carte
        
    Returns:
        QWidget: Un widget CardFrame ou un autre QWidget selon le type d'objet
    """
    if obj is None:
        return QLabel("None")
    
    # Cas scalaires (str, int, float)
    if isinstance(obj, str):
        return QLabel(obj)
    elif isinstance(obj, (int, float)):
        return QLabel(str(obj))
    
    # Cas listes et tuples
    elif isinstance(obj, (list, tuple)):
        if len(obj) == 0:
            return QLabel("Liste vide")
        
        # Si tous les éléments sont de type scalaire, on crée un tableau
        if all(isinstance(item, (str, int, float)) for item in obj):
            table = QTableWidget(len(obj), 1)
            table.setHorizontalHeaderLabels(["Valeurs"])
            for i, item in enumerate(obj):
                table.setItem(i, 0, QTableWidgetItem(str(item)))
            return table
        
        # Sinon, créer une carte pour chaque élément complexe
        container = QWidget()
        layout = QVBoxLayout(container)
        for i, item in enumerate(obj):
            card = object_to_cardframe(item, parent, f"Item {i}")
            layout.addWidget(card)
        container.setLayout(layout)
        return container
    
    # Cas dictionnaires et classes
    elif isinstance(obj, dict) or hasattr(obj, "__dict__"):
        card = CardFrame(parent=parent)
        
        # Déterminer les attributs de l'objet
        if isinstance(obj, dict):
            attributes = obj
            class_name = "Dictionnaire"
        else:
            attributes = {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}
            class_name = obj.__class__.__name__
        
        # Configurer le titre (priorité au titre passé en paramètre)
        if title:
            card.setTopCard(QLabel(title))
        else:
            card.setTopCard(QLabel(class_name))
        
        # Créer des widgets pour les attributs
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        
        for key, value in attributes.items():
            # Pour les types simples, afficher dans le center
            if isinstance(value, (str, int, float)):
                label = QLabel(f"{key}: {value}")
                center_layout.addWidget(label)
            # Pour les listes, afficher le nombre d'éléments
            elif isinstance(value, (list, tuple)):
                label = QLabel(f"{key}: {len(value)} élément(s)")
                center_layout.addWidget(label)
            # Pour les types complexes, créer une carte récursivement
            elif isinstance(value, (dict)) or hasattr(value, "__dict__"):
                nested_card = object_to_cardframe(value, parent, key)
                center_layout.addWidget(nested_card)
        
        center_widget.setLayout(center_layout)
        card.setCenterCard(center_widget)
        
        return card
    
    # Cas par défaut
    else:
        return QLabel(str(obj))

def interfaces_to_cardframe(interface_obj, parent=None) -> QWidget:
    """
    Fonction spécifique pour convertir un objet Interfaces en CardFrame.
    
    Args:
        interface_obj: Instance de la classe Interfaces
        parent: Widget parent
        
    Returns:
        QWidget: Un widget CardFrame représentant l'interface
    """
    card = CardFrame(parent=parent)
    
    # Configuration du titre
    card.setTopCard(QLabel(f"Interface: {interface_obj.alias}"))
    
    # Centre avec les détails
    center_widget = QWidget()
    center_layout = QVBoxLayout(center_widget)
    
    filename_label = QLabel(f"Nom du fichier: {interface_obj.name_file}")
    path_label = QLabel(f"Chemin: {interface_obj.path}")
    
    center_layout.addWidget(filename_label)
    center_layout.addWidget(path_label)
    center_widget.setLayout(center_layout)
    
    card.setCenterCard(center_widget)
    
    return card

class DemoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Démo CardFrame")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        # Créer quelques objets Interfaces
        interface1 = Interfaces(
            name_file="config.json",
            alias="Configuration principale",
            path="/usr/local/etc/app/config.json"
        )
        
        interface2 = Interfaces(
            name_file="settings.ini",
            alias="Paramètres utilisateur",
            path="/home/user/.config/app/settings.ini"
        )
        
        # Créer une structure plus complexe
        complex_data = {
            "config": interface1,
            "settings": interface2,
            "options": ["debug", "verbose", "quiet"],
            "version": 1.2,
            "active": True
        }
        
        # Convertir en CardFrames
        card1 = interfaces_to_cardframe(interface1)
        main_layout.addWidget(card1)
        
        card2 = object_to_cardframe(complex_data, title="Configuration complète")
        main_layout.addWidget(card2)
        
        # Liste d'interfaces
        interfaces_list = [interface1, interface2]
        card3 = object_to_cardframe(interfaces_list, title="Liste des interfaces")
        main_layout.addWidget(card3)
        
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication([])
    window = DemoApp()
    window.show()
    app.exec_()