from pysnmp.smi import builder, view, compiler
from pysnmp.smi.rfc1902 import ObjectIdentity

"""
    Problématique :
    Dans note.py on a un retour de
        "Erreur lors du chargement du module IP-MIB :
        IP-MIB compilation error(s): missing caused by <class 'pysnmp.smi.error.MibNotFoundError'>:
        MIB file "IP-MIB.py[co]" not found in search path
        (DirMibSource('C:\\Users\\g.tronche\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\pysnmp\\smi\\mibs'),
        DirMibSource('C:\\Users\\g.tronche\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\pysnmp\\smi\\mibs\\instances'),
        DirMibSource('pysnmp_mibs'), DirMibSource('C:\\Users\\g.tronche\\PySNMP Configuration\\mibs'))"
    Découpage :
    - problème de chemin d'accès au fichier MIB
    - problème de recherche du fichier MIB
    - problème de compilation du fichier MIB
    - problème de chargement du module MIB

    Solution :
    - J'ai téléchargé un dossier de MIBs déjà compilés en python
    - je n'ai pas trouvé de solution pour pointé vers ce dossier

    """

# chemin d'accès au dossier de MIB au format python
VAR_SRC_MIBS = 'file://D:/lan_audacity/backup/dev/py_mibs'

# Charger les fichiers MIB
mibBuilder = builder.MibBuilder()
mibBuilder.add_mib_sources(builder.DirMibSource('D:/lan_audacity/backup/dev/py_mibs'))
mib_view = view.MibViewController(mibBuilder)

oid = ObjectIdentity('1.3.6.1.2.1.4.24.3.0')
oid.resolve_with_mib(mib_view)
pretty_name = ".".join(map(str, oid.get_label()))
print(oid.get_oid())
print(pretty_name)