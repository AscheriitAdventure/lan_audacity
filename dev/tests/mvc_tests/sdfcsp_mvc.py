from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
import logging
import inspect

# ================== Modèle ==================
@dataclass
class FieldState:
    """Classe de données pour l'état d'un champ"""
    title: str
    form_list: Optional[str] = None
    visible: bool = True
    collapsed: bool = False
    widget: Optional[QWidget] = None
    description: Optional[str] = None
    tooltip: Optional[str] = None
    actions: List[Callable] = field(default_factory=list)
    slots: List[Callable] = field(default_factory=list)

class SDFSPModel:
    """Modèle pour la gestion des données"""
    def __init__(self):
        self.templates: Dict[str, Dict] = {}
        self.active_fields: List[FieldState] = []
        self.current_template: Optional[str] = None

    def register_template(self, name: str, template: Dict):
        """Enregistre un nouveau template"""
        self.templates[name] = template

    def load_template(self, template_name: str) -> Optional[Dict]:
        """Charge un template par son nom"""
        if template_name in self.templates:
            self.current_template = template_name
            return self.templates[template_name]
        return None

    def get_field_state(self, title: str) -> Optional[FieldState]:
        """Récupère l'état d'un champ"""
        return next((field for field in self.active_fields if field.title == title), None)

    def update_field_state(self, title: str, **kwargs) -> bool:
        """Met à jour l'état d'un champ"""
        field = self.get_field_state(title)
        if field:
            for key, value in kwargs.items():
                if hasattr(field, key):
                    setattr(field, key, value)
            return True
        return False

    def add_field_state(self, field_state: FieldState):
        """Ajoute un nouvel état de champ"""
        self.active_fields.append(field_state)

# ================== Vue ==================
class TitleBlock(QWidget):
    """Widget pour le bloc de titre"""
    visibility_clicked = Signal()  # Signal pour le clic sur le bouton de visibilité

    def __init__(self, text: str, show_visibility: bool = False, actions: Optional[List[QPushButton]] = None):
        super().__init__()
        self.setFixedHeight(25)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)

        self.title_label = QLabel(text.upper())
        layout.addWidget(self.title_label)
        layout.addStretch()

        # Ajout du bouton de visibilité si demandé
        if show_visibility:
            visibility_btn = QPushButton("👁")
            visibility_btn.setFixedSize(16, 16)
            visibility_btn.setStyleSheet("QPushButton { border: none; }")
            visibility_btn.clicked.connect(self.visibility_clicked.emit)
            layout.addWidget(visibility_btn)

        if actions:
            for action in actions:
                layout.addWidget(action)

class SDFSPView(QWidget):
    """Vue principale"""
    field_clicked = Signal(str)  # Signal émis lors du clic sur un champ
    state_changed = Signal(str, dict)  # Signal émis lors d'un changement d'état
    
    def __init__(self, debug: bool = False):
        super().__init__()
        self.debug = debug
        self.field_widgets = {}
        self.setup_ui()

    def setup_ui(self):
        """Configuration initiale de l'interface"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(2)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(2, 2, 2, 2)
        self.content_layout.setSpacing(2)

        self.scroll_area.setWidget(self.content_widget)
        self.main_layout.addWidget(self.scroll_area)

    def create_field_widget(self, field_data: FieldState) -> QWidget:
        """Crée un widget pour un champ"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(4, 0, 4, 0)
        layout.setSpacing(1)

        # Création du bouton collapse
        collapse_btn = QPushButton("↓" if not field_data.collapsed else "→")
        collapse_btn.setFixedSize(20, 20)
        collapse_btn.setStyleSheet("QPushButton { border: none; }")

        # Création du header avec le titre
        header = TitleBlock(field_data.title, actions=[collapse_btn])
        layout.addWidget(header)

        # Création du widget principal selon le type
        if field_data.form_list == "tree-file":
            field_widget = QTreeWidget()
        elif field_data.form_list == "list-btn":
            field_widget = QListWidget()
        else:
            field_widget = QWidget()

        layout.addWidget(field_widget)
        field_data.widget = field_widget  # Stocke le widget dans l'état

        # Configuration de la visibilité initiale
        field_widget.setVisible(not field_data.collapsed)
        container.setVisible(field_data.visible)

        # Gestion du collapse
        def toggle_collapse():
            new_collapsed = not field_data.collapsed
            field_widget.setVisible(not new_collapsed)
            collapse_btn.setText("→" if new_collapsed else "↓")
            self.state_changed.emit(field_data.title, {"collapsed": new_collapsed})

        collapse_btn.clicked.connect(toggle_collapse)

        # Stockage du widget pour référence future
        self.field_widgets[field_data.title] = container

        return container

    def update_field_visibility(self, title: str, visible: bool):
        """Met à jour la visibilité d'un champ"""
        if title in self.field_widgets:
            self.field_widgets[title].setVisible(visible)

# ================== Contrôleur ==================
class SDFSPController:
    """Contrôleur principal"""
    def __init__(self, model: SDFSPModel, view: SDFSPView):
        self.model = model
        self.view = view
        self.setup_connections()

    def setup_connections(self):
        """Configure les connexions entre les signaux et les slots"""
        self.view.field_clicked.connect(self.handle_field_click)
        self.view.state_changed.connect(self.handle_state_change)

    def load_template(self, template_name: str):
        """Charge et affiche un template"""
        template_data = self.model.load_template(template_name)
        if template_data:
            self.clear_current_view()
            self.display_template(template_data)

    def clear_current_view(self):
        """Nettoie la vue actuelle"""
        self.model.active_fields.clear()
        for i in reversed(range(self.view.content_layout.count())):
            widget = self.view.content_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def display_template(self, template: Dict):
        """Affiche un template dans la vue"""
        # Ajout du titre du stack avec le bouton de visibilité si plusieurs champs
        show_visibility = len(template.get("fields", [])) > 1
        title_block = TitleBlock(template.get("stacked_title", "Untitled"), show_visibility=show_visibility)
        
        if show_visibility:
            title_block.visibility_clicked.connect(
                lambda: self.show_visibility_menu(template.get("fields", []))
            )
        
        self.view.content_layout.addWidget(title_block)

        # Ajout du séparateur si nécessaire
        if template.get("separator", False):
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            self.view.content_layout.addWidget(separator)

        # Création des champs
        for field_data in template.get("fields", []):
            field_state = FieldState(
                title=field_data["title"],
                form_list=field_data.get("form_list"),
                visible=field_data.get("visible", True),
                collapsed=field_data.get("collapsed", False),
                description=field_data.get("description"),
                tooltip=field_data.get("tooltip"),
                actions=field_data.get("actions", []),
                slots=field_data.get("slots", [])
            )
            self.model.add_field_state(field_state)
            
            field_widget = self.view.create_field_widget(field_state)
            self.view.content_layout.addWidget(field_widget)

    def handle_field_click(self, field_title: str):
        """Gère les clics sur les champs"""
        field = self.model.get_field_state(field_title)
        if field and field.actions:
            for action in field.actions:
                if callable(action):
                    action()

    def handle_state_change(self, field_title: str, changes: Dict):
        """Gère les changements d'état des champs"""
        if self.model.update_field_state(field_title, **changes):
            # Met à jour la visibilité du widget si nécessaire
            if "visible" in changes:
                self.view.update_field_visibility(field_title, changes["visible"])

    def show_visibility_menu(self, fields: List[Dict]):
        """Affiche le menu de visibilité des champs"""
        menu = QMenu(self.view)
        for field in fields:
            title = field.get("title")
            action = QAction(title, menu)
            action.setCheckable(True)
            
            # Récupère l'état actuel du champ
            field_state = self.model.get_field_state(title)
            if field_state:
                action.setChecked(field_state.visible)

                def make_toggle_func(ftitle):
                    def toggle_visibility(checked):
                        # Vérifie qu'au moins un champ reste visible
                        visible_count = sum(
                            1 for f in self.model.active_fields if f.visible
                        )
                        if not checked and visible_count <= 1:
                            action.setChecked(True)
                            return
                        # Met à jour l'état et la visibilité
                        self.handle_state_change(ftitle, {"visible": checked})
                    return toggle_visibility

                action.triggered.connect(make_toggle_func(title))
            menu.addAction(action)

        # Affiche le menu
        menu.exec_(QCursor.pos())

# ================== Exemple d'utilisation ==================
def demo_action():
    print("Action déclenchée")

DEFAULT_TEMPLATE = {
    "stacked_title": "Démo Default",
    "separator": True,
    "shortcut": "Ctrl+D",
    "enable": True,
    "fields": [
        {
            "title": "Explorateur",
            "form_list": "tree-file",
            "separator": True,
            "collapsed": False,
            "tooltip": "Explorateur de fichiers",
            "actions": [demo_action],
            "description": "Navigation dans les fichiers",
            "visible": True,
            "slots": []
        },
        {
            "title": "Liste",
            "form_list": "list-btn",
            "separator": False,
            "collapsed": False,
            "tooltip": "Liste d'éléments",
            "actions": [demo_action],
            "description": "Liste simple",
            "visible": True,
            "slots": []
        }
    ]
}

def main():
    app = QApplication([])
    
    # Création des composants MVC
    model = SDFSPModel()
    view = SDFSPView(debug=True)
    controller = SDFSPController(model, view)

    # Enregistrement et chargement du template
    model.register_template("default", DEFAULT_TEMPLATE)
    controller.load_template("default")

    # Affichage de la fenêtre
    view.resize(300, 600)
    view.show()
    
    app.exec_()

if __name__ == "__main__":
    main()