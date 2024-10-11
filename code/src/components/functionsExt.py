import os
import logging
import time

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
    mask_octets = list(map(int, mask.split('.')))

    # Convert the subnet mask into its binary representation and count the number of 1s
    mask_binary_str = ''.join(format(octet, '08b') for octet in mask_octets)
    cidr_prefix = mask_binary_str.count('1')

    # Combine the IP address with the CIDR prefix to form the CIDR notation
    cidr_notation = f"{ip}/{cidr_prefix}"

    return cidr_notation

def cidr_to_ip(cidr: str) -> tuple:
    # Split the CIDR notation into the IP address and the CIDR prefix
    ip, cidr_prefix = cidr.split('/')

    # Split the IP address into its octets and convert them into integers
    ip_octets = list(map(int, ip.split('.')))

    # Calculate the number of bits in the subnet mask
    cidr_prefix = int(cidr_prefix)
    cidr_suffix = 32 - cidr_prefix

    # Calculate the subnet mask in binary representation
    mask_binary_str = '1' * cidr_prefix + '0' * cidr_suffix

    # Split the binary representation into octets and convert them into integers
    mask_octets = [int(mask_binary_str[i:i + 8], 2) for i in range(0, 32, 8)]

    return tuple(ip_octets), tuple(mask_octets)

def conv_unix_to_datetime(unix_time: float):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(unix_time))