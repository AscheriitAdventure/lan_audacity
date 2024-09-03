import os
import logging

def current_dir():
    try:
        curr_path = os.getcwd()
        return curr_path
    except Exception as e:
        logging.error(
            f"Une erreur s'est produite lors de l'obtention du répertoire de travail actuel : {e}"
        )
        return "Analyse Erreur"


def get_spcValue(liste_add: list, arg_1: str, obj_src: str) -> dict:
    for obj_dict in liste_add:
        if obj_dict[arg_1] == obj_src:
            return obj_dict
    return {}

def ip_to_cidr(ip: str, mask: str) -> str:
    # Split the IP address and the subnet mask into their respective octets
    ip_octets = list(map(int, ip.split('.')))
    mask_octets = list(map(int, mask.split('.')))

    # Convert the subnet mask into its binary representation and count the number of 1s
    mask_binary_str = ''.join(format(octet, '08b') for octet in mask_octets)
    cidr_prefix = mask_binary_str.count('1')

    # Combine the IP address with the CIDR prefix to form the CIDR notation
    cidr_notation = f"{ip}/{cidr_prefix}"

    return cidr_notation