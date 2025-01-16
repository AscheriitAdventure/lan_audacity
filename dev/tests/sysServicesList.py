from enum import Enum
from typing import List


class ISOLayer(Enum):
    PHYSICAL = 1
    DATA_LINK = 2
    NETWORK = 3
    TRANSPORT = 4
    SESSION = 5
    PRESENTATION = 6
    APPLICATIONS = 7


def sysServicesList(tag_oid: int) -> List[str]:
    """
    Retourne une liste des services (couches OSI) en fonction de la valeur numérique (tag_oid).
    """
    services = []
    if tag_oid == 0:
        services.append("Do not possess this information")
    else:
        for layer in ISOLayer:
            # Vérifie si le bit correspondant à la couche est activé
            if tag_oid & (1 << (layer.value - 1)):
                services.append(layer.name)

    return services


# Exemple d'utilisation
if __name__ == "__main__":
    test_value = 64  # Exemple de valeur à analyser
    result = sysServicesList(test_value)
    print(f"Services for tag_oid {test_value}: {result}")
