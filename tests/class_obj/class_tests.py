import re

def prettyKeys(obj: object) -> dict:
    """
    renvoi un dictionnaire de joli clefs ex:
        entrée object
            {'attribut1': 'Hello', '_HW__attribut2': 'World', '_HW__attribut3': '!'}
        sortie {'attribut1': 'Attribut 1', '_HW__attribut2': 'Attribut 2', '_HW__attr33ibut': 'Attr 33 Ibut'}
    """
    pretty_keys: dict = dict()
    
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
    print(f"Pretty list: {prettyKeysList(HW())}")
    s = HW()
    print(f"class name: {s.__class__.__name__}\n")  # class name: HW
    print(f"class dict: {s.__dict__}\n")

    pretty_dict = prettyKeys(s)
    print(f"Pretty dict: {pretty_dict}")

    pretty_list = prettyKeysList(s)
    print(f"Pretty list: {pretty_list}")