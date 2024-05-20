import ipaddress


def cidr_to_ip_mask(cidr):
    try:
        # Séparer l'adresse CIDR en adresse IP et préfixe
        ip, prefix = cidr.split('/')

        # Convertir le préfixe en masque de sous-réseau
        subnet_mask = ipaddress.IPv4Network(cidr).netmask

        # Renvoyer l'adresse IP et le masque sous forme de tuple de chaînes de caractères
        return ip, str(subnet_mask)
    except ValueError:
        # En cas d'erreur de format CIDR
        print("Format CIDR invalide.")
        return None, None


# Exemple d'utilisation
cidr = "192.168.1.0/24"
ip, mask = cidr_to_ip_mask(cidr)
print("Adresse IP:", ip)
print("Masque de sous-réseau:", mask)
