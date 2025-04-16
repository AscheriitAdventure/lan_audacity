def prettyKeys(obj: object) -> dict:
    """
    renvoi un dictionnaire de joli clefs ex:
        entrée object
            {'attribut1': 'Hello', '_HW__attribut2': 'World', '_HW__attribut3': '!'}
        sortie {'attribut1': 'Attribut 1', '_HW__attribut2': 'Attribut 2', '_HW__attr33ibut': 'Attr 33 Ibut'}
    """
    origin_d = obj.__dict__
    tmp_d: dict = dict()

    for k, v in origin_d.items():
        original_key = k
        new_value = k

        if obj.__class__.__name__ in new_value:
            # Suppression du nom de la classe
            new_value = new_value.replace(f"_{obj.__class__.__name__}", "")

        # Si le nom de la variable commence par un ou plusieurs underscore, on les supprime
        new_value = new_value.lstrip('_')

        # Si le nom de la variable possède un ou plusieurs underscore, on les remplace par un espace
        new_value = new_value.replace('_', ' ')

        # Si le nom de la variable possède des chiffres collés à une suite de lettres,
        # on ajoute un espace entre les lettres et les chiffres
        import re
        new_value = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', new_value)
        new_value = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', new_value)

        # Pour finir tous les mots > 2 lettres commencent par une majuscule
        words = new_value.split()
        capitalized_words = []

        for word in words:
            if len(word) > 2:
                capitalized_words.append(word.capitalize())
            else:
                capitalized_words.append(word)

        # Ajouter un espace avant les chiffres à la fin
        base_name = ''.join(capitalized_words)
        # Extraire les chiffres à la fin du nom
        match = re.search(r'(\d+)$', original_key)
        if match:
            number = match.group(1)
            base_name = re.sub(r'\d+$', '', base_name)
            new_value = f"{base_name} {number}"
        else:
            # Si pas de chiffre à la fin, vérifier si on peut en trouver dans le nom
            match = re.search(r'(\d+)', original_key)
            if match:
                number = match.group(1)
                parts = re.split(r'\d+', base_name, maxsplit=1)
                if len(parts) > 1:
                    new_value = f"{parts[0]} {number} {parts[1]}"
                else:
                    new_value = f"{parts[0]} {number}"
            else:
                # Si pas de chiffres du tout, ajouter l'index de la clé
                index = list(origin_d.keys()).index(original_key) + 1
                new_value = f"{base_name} {index}"

        tmp_d[original_key] = new_value

    return tmp_d


class HW(object):
    def __init__(self):
        self.attribut1: str = "Hello"
        self.__attribut2: str = "World"
        self.__attr33ibut: str = "!"


if __name__ == '__main__':
    s = HW()
    print(f"class name: {s.__class__.__name__}\n")  # class name: HW
    print(f"class dict: {s.__dict__}\n")

    pretty_dict = prettyKeys(s)
    print(f"Pretty dict: {pretty_dict}")