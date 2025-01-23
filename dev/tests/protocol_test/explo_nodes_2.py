"""
    1. Création de fonctions:
        - Fonction Objet: 
          Question: Qui est connecté sur le réseau?
          Retour asynchrone: une adresse ip (v4 ou v6)
          Nom de la fonction: who_is_there
          Paramètres: Rien ou range d'adresses ip
        - Fonction Objet:
          Question: Es tu encore là?
          Retour: Oui ou Non
          Nom de la fonction: are_you_still_there
          Paramètres: Une adresse ip (v4 ou v6) et une fréquence en ms
        - Fonction Objet:
          Question: Qui es tu?
          Retour: Nom du node
          Nom de la fonction: who_are_you
          Paramètres: Une adresse ip (v4 ou v6)
        - Fonction Objet:

    2. 
"""
from typing import List, Optional, Union, Tuple
from icmplib import ping, multiping, resolve, Host, NameLookupError
from concurrent.futures import ThreadPoolExecutor
import ipaddress
import asyncio
import socket
from time import sleep

def icmp_explo_nodes() -> List[str]:
    """
    Exploration des nodes avec ICMP et retourne la liste des nodes actifs
    sur le réseau local (192.168.1.0/24 par défaut)
    
    Returns:
        List[str]: Liste des adresses IP des nodes actifs
    """
    network = "192.168.1.0/24"
    addresses = [str(ip) for ip in ipaddress.IPv4Network(network)]
    active_hosts = []
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        hosts = list(executor.map(
            lambda addr: ping(addr, count=1, timeout=1, privileged=False),
            addresses
        ))
        
        for host, addr in zip(hosts, addresses):
            if host.is_alive:
                active_hosts.append(addr)
                
    return active_hosts

async def who_is_there(ip_range: Optional[str] = None) -> List[str]:
    """
    Détecte les hôtes actifs sur le réseau
    
    Args:
        ip_range (Optional[str]): Range d'adresses IP (ex: "192.168.1.0/24")
                                 Si None, utilise le réseau local par défaut
    
    Returns:
        List[str]: Liste des adresses IP des hôtes actifs
    """
    if ip_range is None:
        ip_range = "192.168.1.0/24"
        
    try:
        network = ipaddress.ip_network(ip_range)
        addresses = [str(ip) for ip in network]
        hosts = await asyncio.create_task(multiping(addresses, count=1, timeout=1))
        return [str(host.address) for host in hosts if host.is_alive]
    except ValueError:
        raise ValueError(f"Format de range IP invalide: {ip_range}")

def are_you_still_there(ip: str, frequency_ms: int = 1000) -> bool:
    """
    Vérifie si un hôte est toujours accessible
    
    Args:
        ip (str): Adresse IP de l'hôte à vérifier
        frequency_ms (int): Fréquence de vérification en millisecondes
    
    Returns:
        bool: True si l'hôte répond, False sinon
    """
    try:
        ipaddress.ip_address(ip)  # Validation de l'adresse IP
        sleep(frequency_ms / 1000.0)  # Conversion ms en secondes
        host = ping(ip, count=1, timeout=1, privileged=False)
        return host.is_alive
    except ValueError:
        raise ValueError(f"Adresse IP invalide: {ip}")

def who_are_you(ip: str) -> Optional[str]:
    """
    Récupère le nom d'hôte d'une adresse IP
    
    Args:
        ip (str): Adresse IP de l'hôte
    
    Returns:
        Optional[str]: Nom d'hôte ou None si non trouvé
    """
    try:
        ipaddress.ip_address(ip)  # Validation de l'adresse IP
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except (socket.herror, socket.gaierror):
            return None
    except ValueError:
        raise ValueError(f"Adresse IP invalide: {ip}")
    
# Exploration des nodes avec nmap
# Exploration des nodes avec SNMP
# Exploration des nodes avec SSH