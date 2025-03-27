import enum

# Classe pour la table OSILayer
class OSILayer(enum.Enum):
    APPLICATION = 7
    PRESENTATION = 6
    SESSION = 5
    TRANSPORT = 4
    NETWORK = 3
    DATA_LINK = 2
    PHYSICAL = 1