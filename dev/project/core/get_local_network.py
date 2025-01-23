import netifaces
import ipaddress
from typing import List, Set
import logging


def get_local_network(include_link_local: bool = True) -> List[str]:
    """
    Récupère l'adresse du réseau local au format CIDR.

    Args:
        include_link_local (bool): Si True, inclut les réseaux de liaison locale (fe80::/10).

    Returns:
        List[str]: Liste des adresses réseau uniques au format CIDR.
    """
    # Utilisation d'un set pour garantir l'unicité des réseaux
    unique_networks: Set[str] = set()

    for interface in netifaces.interfaces():
        try:
            addresses = netifaces.ifaddresses(interface)

            # Gérer les adresses IPv4
            if netifaces.AF_INET in addresses:
                for addr_info in addresses[netifaces.AF_INET]:
                    logging.debug(f"IPv4 info for {interface}: {addr_info}")
                    ip_addr = addr_info.get('addr')
                    netmask = addr_info.get('netmask')
                    if ip_addr and netmask:
                        try:
                            network = ipaddress.IPv4Network(
                                f"{ip_addr}/{netmask}", strict=False)
                            unique_networks.add(str(network))
                        except ipaddress.NetmaskValueError:
                            logging.warning(f"Invalid IPv4 netmask for {ip_addr}: {netmask}")

            # Gérer les adresses IPv6
            if netifaces.AF_INET6 in addresses:
                for addr_info in addresses[netifaces.AF_INET6]:
                    logging.debug(f"IPv6 info for {interface}: {addr_info}")
                    ip_addr = addr_info.get('addr')
                    netmask = addr_info.get('netmask')
                    if ip_addr and netmask:
                        try:
                            # Supprimer la partie après '%' (zone ID) dans l'adresse IPv6
                            ip_addr = ip_addr.split('%')[0]
                            # Extraire le préfixe du masque
                            prefix_length = netmask.split(
                                '/')[1] if '/' in netmask else '64'
                            network = ipaddress.IPv6Network(
                                f"{ip_addr}/{prefix_length}", strict=False)
                            # Ajouter les réseaux de liaison locale si autorisé
                            if include_link_local or not network.is_link_local:
                                unique_networks.add(str(network))
                        except (ipaddress.NetmaskValueError, ValueError) as e:
                            logging.warning(
                                f"Invalid IPv6 address/netmask for {ip_addr}: {e}")

        except Exception as error:
            logging.error(f"Error processing interface {interface}: {error}")

    # Convertir le set en liste et trier pour une sortie cohérente
    return sorted(list(unique_networks))


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.DEBUG)
#     networks = get_local_network()
#     print("\nRéseaux détectés :")
#     for network in networks:
#         print(f"- {network}")
