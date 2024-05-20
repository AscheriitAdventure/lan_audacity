import nmap

# Récupère tous les hôtes du réseau
all_hosts = []
nm = nmap.PortScanner()
# équivalent à nmap -sn
nm.scan(hosts="192.168.1.0/24", arguments="-sn")
for host in nm.all_hosts():
    all_hosts.append(host)

print(all_hosts)


# Avec une adresse IPv4 récupérer l'adresse IPv6 correspondante
def ipv4_to_ipv6(ipv4_address):
    nm = nmap.PortScanner()
    try:
        # Utilisez nmap pour scanner l'adresse IPv4 spécifiée
        nm.scan(hosts=ipv4_address, arguments="-sn")
        # Récupère toutes les adresses IPv6 détectées pour l'adresse IPv4 spécifiée
        ipv6_addresses = nm[ipv4_address]["addresses"].get("ipv6", None)
        return ipv6_addresses
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return None


ipv6_address = ipv4_to_ipv6(all_hosts[1])
if ipv6_address:
    print(f"L'adresse IPv6 correspondante pour {all_hosts[1]} est : {ipv6_address}")
else:
    print(f"Aucune adresse IPv6 correspondante n'a été trouvée pour {all_hosts[1]}.")

## Récupère toutes les adresses IPv6 du réseau
# all_ipv6 = []
# nm = nmap.PortScanner()
## équivalent à nmap -6 -sn
# nm.scan(hosts="fe80::/64", arguments="-6 -sn")
# for host in nm.all_hosts():
#     all_ipv6.append(host)

# print(all_ipv6)
