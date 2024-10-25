dictionnaire = {
    "ipv4": "192.168.1.90",
    "mask_ipv4": "255.255.255.0",
    "cidr": "192.168.1.90/24",
    "ipv6_local": "fe80::c0a8:1:5a",
    "ipv6_global": "fe80::c0a8:1:5a",
}

# Récupérer les entêtes (clés) du dictionnaire
entetes = dictionnaire.keys()

# Afficher les entêtes
print("Les entêtes du dictionnaire sont :", list(entetes))
