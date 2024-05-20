import netifaces

def netmask_to_cidr(netmask):
    # Convertit le masque de sous-réseau en une liste de bits
    bits = sum(bin(int(x)).count('1') for x in netmask.split('.'))
    return bits

ls_net_interface = netifaces.interfaces()
for net_interface in ls_net_interface:
    if netifaces.AF_INET in netifaces.ifaddresses(net_interface):
        addr_info = netifaces.ifaddresses(net_interface)[netifaces.AF_INET]
        for info in addr_info:
            if info.get('addr') != '127.0.0.1':
                print(net_interface)
                cidr = netmask_to_cidr(info.get('netmask'))
                print(f"Netmask: {info.get('netmask')} -> CIDR: /{cidr}")

