import os
from enum import Enum


class TopologyActivity(Enum):
    BLUE = 0 # Unknown
    GREEN = 1 # Active
    RED = 2 # Inactive/Alert
    GRAY = 3 # Disabled

class TopologyForms(Enum):
    CIRCLE = 0 # Default Device
    SQUARE = 1 # Physical Device
    NAKED = 2 # Exist but forbidden to use

class OSILayer(Enum):
    PHYSICAL = 1 # Physical Layer
    DATA_LINK = 2 # Data Link Layer
    NETWORK = 3 # Network Layer
    TRANSPORT = 4 # Transport Layer
    SESSION = 5 # Session Layer
    PRESENTATION = 6 # Presentation Layer
    APPLICATION = 7 # Application Layer

# Affiche le nom de la couche OSI
def osiLayerToString(layer: OSILayer) -> str:
    return {
        OSILayer.PHYSICAL: "Physical",
        OSILayer.DATA_LINK: "Data Link",
        OSILayer.NETWORK: "Network",
        OSILayer.TRANSPORT: "Transport",
        OSILayer.SESSION: "Session",
        OSILayer.PRESENTATION: "Presentation",
        OSILayer.APPLICATION: "Application"
    }[layer]

# Affiche le nom de l'activité
def activityToString(activity: TopologyActivity) -> str:
    return {
        TopologyActivity.BLUE: "blue",
        TopologyActivity.GREEN: "green",
        TopologyActivity.RED: "red",
        TopologyActivity.GRAY: "gray"
    }[activity]

# Affiche le nom de la forme
def formToString(form: TopologyForms) -> str:
    return {
        TopologyForms.CIRCLE: "circle",
        TopologyForms.SQUARE: "square",
        TopologyForms.NAKED: "naked"
    }[form]

# Conditions de sélection des images (svg)
def getNetworkDeviceImage(form: TopologyForms, activity: TopologyActivity, nme_img: str) -> str:
    if form == TopologyForms.CIRCLE:
        if activity == TopologyActivity.GREEN:
            return os.path.join("affinity", "svg", "circle", "green", nme_img)
        elif activity == TopologyActivity.RED:
            return os.path.join("affinity", "svg", "circle", "red", nme_img)
        elif activity == TopologyActivity.GRAY:
            return os.path.join("affinity", "svg", "circle", "gray", nme_img)
        else:
            return os.path.join("affinity", "svg", "circle", "blue", nme_img)
    elif form == TopologyForms.SQUARE:
        if activity == TopologyActivity.GREEN:
            return os.path.join("affinity", "svg", "square", "green", nme_img)
        elif activity == TopologyActivity.RED:
            return os.path.join("affinity", "svg", "square", "red", nme_img)
        elif activity == TopologyActivity.GRAY:
            return os.path.join("affinity", "svg", "square", "gray", nme_img)
        else:
            return os.path.join("affinity", "svg", "square", "blue", nme_img)
    else:
        return os.path.join("affinity", "svg", "naked", nme_img)


image_path = os.path.join(
    "C:/Users", "g.tronche", "Documents", "GitHub", 
    getNetworkDeviceImage(TopologyForms(0), TopologyActivity(0), "c_bug.svg"))

# Vérification de l'existence du fichier
if os.path.exists(image_path):
    print("Le fichier existe")

# Affichage du chemin sans le nom du fichier
print(os.path.dirname(image_path))

# liste le nombre de fichiers dans le répertoire
print(len(os.listdir(os.path.dirname(image_path))))

img_pth2 = os.path.join(
    "C:/Users", "g.tronche", "Documents", "GitHub", 
    getNetworkDeviceImage(TopologyForms(0), TopologyActivity(3), "c_bug.svg"))

# Comparaison de deux répertoire
if os.path.dirname(image_path) == os.path.dirname(img_pth2):
    print("Les répertoires sont identiques")
else:
    print("Les répertoires sont différents")