import logging
import inspect
from typing import *
import nmap
import os
import socket
import struct
import time
import select

from src.models import *

# Fonction pour calculer le checksum ICMP
def calculate_checksum(data):
    checksum = 0
    count_to = (len(data) // 2) * 2

    for i in range(0, count_to, 2):
        checksum += (data[i + 1] << 8) + data[i]

    if count_to < len(data):
        checksum += data[count_to]

    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum += (checksum >> 16)

    return ~checksum & 0xffff

# Créer un paquet ICMP Echo Request
def create_icmp_packet():
    # Type 8: Echo Request, Code 0
    icmp_type = 8
    icmp_code = 0
    icmp_checksum = 0
    icmp_id = os.getpid() & 0xFFFF  # ID basé sur le PID
    icmp_seq = 1

    # En-tête ICMP (8 octets) + données (8 octets pour timestamp)
    header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
    data = struct.pack("!d", time.time())

    # Calculer le checksum avec une en-tête temporaire
    icmp_checksum = calculate_checksum(header + data)

    # Recréer l'en-tête avec le checksum correct
    header = struct.pack("!BBHHH", icmp_type, icmp_code, socket.htons(icmp_checksum), icmp_id, icmp_seq)

    return header + data


class SwitchFunctions:
    def speedScan(self, cidr_addr: str) -> list:
        """
        Scan the network for devices and return a list of their IP addresses.

        Args:
            cidr_addr (str): CIDR address to scan.

        Returns:
            list: List of IP addresses of devices found in the scan.
        """
        nmap_ls = list()
        try:
            nm = nmap.PortScanner()
            nm.scan(hosts=cidr_addr, arguments="-sn")
            for host in nm.all_hosts():
                if nm[host].state() == "up":
                    nmap_ls.append(host)
        except Exception as e:
            msg = f"Error during network scan - {str(e)}"
            db_msg = f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}::{inspect.currentframe().f_lineno}: "
            logging.error(db_msg + msg)

        return nmap_ls

    def icmpScan(self, ip_addr: str) -> list:
        """
        Perform an ICMP scan on the specified IP address.

        Args:
            ip_addr (str): IP address to scan.

        Returns:
            list: List containing the IP address if it responds, otherwise empty list.
        """
        # Liste pour stocker l'adresse IP si elle répond
        live_hosts = []
    
        # Créer un socket raw ICMP
        if os.name == "nt":  # Windows nécessite un traitement spécial
            icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        else:
            # Linux et autres systèmes Unix/Unix-like
            icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    
        # Définir le timeout du socket
        icmp_socket.settimeout(1)

        # Créer le paquet ICMP une seule fois
        packet = create_icmp_packet()
    
        try:
            # Envoyer le paquet ICMP à l'adresse IP
            icmp_socket.sendto(packet, (ip_addr, 0))
        
            # Attendre une réponse avec select (plus efficace qu'un simple timeout)
            ready = select.select([icmp_socket], [], [], 1)
        
            if ready[0]:
                # Recevoir la réponse
                recv_packet, addr = icmp_socket.recvfrom(1024)
            
                # Vérifier si la réponse vient de l'adresse IP ciblée
                if addr[0] == ip_addr:
                    live_hosts.append(ip_addr)

        except (socket.timeout, socket.error) as e:
            msg = f"Erreur lors du scan de {ip_addr}: {e}"
            db_msg = f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}::{inspect.currentframe().f_lineno}: "
            logging.error(db_msg + msg)

        finally:
            # Fermer le socket
            icmp_socket.close()
    
        return live_hosts

    def fullPortScan(self, var_uc: Device) -> list:
        res: List[PortsObject] = list()

        nm = nmap.PortScanner()
        nm.scan(hosts=var_uc.web_address.ipv4, arguments="-sV -p 1-65535 -v --max-retries 0 --host-timeout 3m")

        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                for port in lport:
                    tmp_d = dict()
                    tmp_d["port_number"] = port
                    tmp_d["device"] = var_uc
                    tmp_d["protocol"] = proto
                    tmp_d["port_status"] = nm[host][proto][port]["state"]
                    tmp_d["port_service"] = nm[host][proto][port]["name"]
                    tmp_d["port_version"] = nm[host][proto][port]["version"]
                    res.append(PortsObject(**tmp_d).get_dict())
        
        return res
    
    def fullOsScan(self, var_uc: Device) -> list:
        res: list = list()
        tmp_d = dict()
        tmp_d["device"] = var_uc

        nm = nmap.PortScanner()
        nm.scan(hosts=var_uc.web_address.ipv4, arguments="-O -A -v --max-retries 0 --host-timeout 1m")

        for host in nm.all_hosts():
            if "osmatch" in nm[host] and len(nm[host]["osmatch"]) > 0:
                logging.debug(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: OS match found for {host}: {nm[host]['osmatch']}")
                for osmatch in nm[host]["osmatch"]:
                    tmp_d["name_object"] = osmatch.get("name", "")
                    tmp_d["accuracy_int"] = osmatch.get("accuracy", 0)
                    res.append(OSAccuracy(**tmp_d).get_dict())

        return res
        
