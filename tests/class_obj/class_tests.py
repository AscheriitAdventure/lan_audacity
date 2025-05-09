import re
from src.models import Device

def prettyKeys(obj: object) -> dict:
    """
    renvoi un dictionnaire de joli clefs ex:
        entrée object
            {'attribut1': 'Hello', '_HW__attribut2': 'World', '_HW__attribut3': '!'}
        sortie {'attribut1': 'Attribut 1', '_HW__attribut2': 'Attribut 2', '_HW__attr33ibut': 'Attr 33 Ibut'}
    """
    pretty_keys: dict = dict()

    if hasattr(obj, '__dict__'):
        keys_dict = obj.__dict__
    elif isinstance(obj, dict):
        keys_dict = obj
    else:
        raise TypeError("L'objet fourni doit être une classe, une dataclass ou un dictionnaire")
    
    for key in keys_dict.keys():
        # Nettoyer le nom (enlever préfixes de classe, underscores)
        if isinstance(obj, dict):
            # Pour les dictionnaires, nous ne pouvons pas utiliser obj.__class__.__name__
            clean_key = key.lstrip('_').replace('_', ' ')
        else:
            if '__' in key and key.startswith('_'):
                # Format pour attributs privés: '_ClassName__attributName'
                clean_key = key.split('__')[1].replace('_', ' ')
            else:
                clean_key = key.replace(f"_{obj.__class__.__name__}__", "").lstrip('_').replace('_', ' ')
        
        # Ajouter espaces avant majuscules et entre chiffres/lettres
        clean_key = re.sub(r'([A-Z])', r' \1', clean_key)
        clean_key = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', clean_key)
        clean_key = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', clean_key)
        
        # Capitaliser le début et les mots longs
        words = [w.capitalize() if len(w) > 2 else w for w in clean_key.split()]
        pretty_key = ' '.join(words).strip()
        
        pretty_keys[key] = pretty_key
    
    return pretty_keys

def prettyKeysList(obj: object) -> list:
    pretty_keys = []
    
    for key in obj.__dict__.keys():
        # Nettoyer le nom (enlever préfixes de classe, underscores)
        clean_key = key.replace(f"_{obj.__class__.__name__}", "").lstrip('_').replace('_', ' ')
        
        # Ajouter espaces avant majuscules et entre chiffres/lettres
        clean_key = re.sub(r'([A-Z])', r' \1', clean_key)
        clean_key = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', clean_key)
        clean_key = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', clean_key)
        
        # Capitaliser le début et les mots longs
        words = [w.capitalize() if len(w) > 2 else w for w in clean_key.split()]
        pretty_key = ' '.join(words).strip()
        
        pretty_keys.append(pretty_key)
    
    return pretty_keys

class HW(object):
    def __init__(self):
        self.attribut: str = "Hello"
        self.__attribut2: str = "World"
        self.__attr33ibut: str = "!"
        self.__5_nameObject: str = "HW!"


if __name__ == '__main__':
    print(f"Pretty list: {prettyKeysList(Device())}")
    s = Device()
    print(f"class name: {s.__class__.__name__}\n")  # class name: HW
    print(f"class dict: {s.__dict__}\n")

    pretty_dict = prettyKeys(s)
    print(f"Pretty dict: {pretty_dict}")
    print(f"Pretty dict: {prettyKeys({'key': None, 'key2': 'value2'})}")

    pretty_list = prettyKeysList(s)
    print(f"Pretty list: {pretty_list}")