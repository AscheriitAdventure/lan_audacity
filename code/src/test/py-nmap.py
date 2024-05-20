import nmap

# Initialiser la classe Nmap
nm = nmap.PortScanner()

# Scanneur le réseau 192.168.1.0/24
nm.scan(hosts="192.168.1.0/24", arguments="-sP")

# Afficher les résultats
for host in nm.all_hosts():
    print(f"Host : {host}")
    for proto in nm[host].all_protocols():
        print(f"  Protocol : {proto}")
        for port in nm[host][proto].keys():
            print(f"    Port : {port} - {nm[host][proto][port]['name']}")