from typing import List, Optional, Union
from icmplib import ping, multiping
from concurrent.futures import ThreadPoolExecutor
import ipaddress
import asyncio

from dev.project.core.get_local_network import get_local_network


def who_is_there(network_cidr: Optional[Union[str, List[str]]] = None) -> List[str]:
    """
    Version synchrone - Détecte les hôtes actifs sur le réseau
    
    Args:
        network_cidr (Optional[str]): Notation CIDR du réseau (ex: "192.168.1.0/24" ou "2001:db8::/64")
                                     Si None, utilise le réseau local par défaut
    
    Returns:
        List[str]: Liste des adresses IP des hôtes actifs
    
    Raises:
        ValueError: Si la notation CIDR est invalide
    """
    if network_cidr is None:
        network_cidr = get_local_network()
    
    if isinstance(network_cidr, str):
        network_cidr = [network_cidr]
    
    active_hosts = []

    for cidr in network_cidr:
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            addresses = [str(ip) for ip in network.hosts()]

            with ThreadPoolExecutor(max_workers=20) as executor:
                results = list(executor.map(
                    lambda addr: ping(addr, count=1, timeout=1, privileged=False),
                    addresses
                ))

                for host, addr in zip(results, addresses):
                    if host.is_alive:
                        active_hosts.append(addr)

        except ValueError as e:
            raise ValueError(f"Format CIDR invalide: {cidr}") from e
    
    return active_hosts

async def who_is_there_async(network_cidr: Optional[Union[str, List[str]]] = None) -> List[str]:
    """
    Version asynchrone - Détecte les hôtes actifs sur le réseau
    
    Args:
        network_cidr (Optional[str]): Notation CIDR du réseau (ex: "192.168.1.0/24" ou "2001:db8::/64")
                                     Si None, utilise le réseau local par défaut
    
    Returns:
        List[str]: Liste des adresses IP des hôtes actifs
    
    Raises:
        ValueError: Si la notation CIDR est invalide
    """
    if network_cidr is None:
        network_cidr = get_local_network()
    
    if isinstance(network_cidr, str):
        network_cidr = [network_cidr]
    
    active_hosts = []

    for cidr in network_cidr:
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            addresses = [str(ip) for ip in network.hosts()]

            # Utilisation de multiping pour les requêtes asynchrones
            hosts = await asyncio.create_task(
                multiping(addresses, count=1, timeout=1, privileged=False)
            )
        
            active_hosts.extend([str(host.address) for host in hosts if host.is_alive])
        except ValueError as e:
            raise ValueError(f"Format CIDR invalide: {cidr}") from e
