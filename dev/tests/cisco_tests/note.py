from pysnmp.smi import builder, view, compiler
from pysnmp.smi.rfc1902 import ObjectIdentity
import os

VAR_SRC_MIBS = 'D:/lan_audacity/backup/dev/py_mibs'

# Charger les fichiers MIB
mibBuilder = builder.MibBuilder()
mibBuilder.add_mib_sources(builder.DirMibSource(VAR_SRC_MIBS))
compiler.add_mib_compiler(mibBuilder, sources=[
                          'http://mibs.snmplabs.com/asn1/@mib@', f'file://{VAR_SRC_MIBS}'])

# Construire un traducteur MIB
mibViewController = view.MibViewController(mibBuilder)


def load_mib_for_oid(oid):
    """Essaye de résoudre un OID, et charge la MIB correspondante s'il échoue"""
    obj = ObjectIdentity(oid)
    try:
        obj.resolve_with_mib(mibViewController)
        return obj.get_label()
    except Exception:
        print(f"OID inconnu : {oid}. Recherche de la MIB correspondante...")

        # Vérifier les fichiers dans VAR_SRC_MIBS pour trouver une MIB qui pourrait contenir cet OID
        for filename in os.listdir(VAR_SRC_MIBS):
            mib_name = filename.rsplit('.', 1)[0]  # Supprime l'extension
            try:
                mibBuilder.load_modules(mib_name)
                print(f"MIB chargée : {mib_name}")

                # Réessayer la résolution après le chargement
                obj.resolve_with_mib(mibViewController)
                return obj.get_label()
            except Exception as e:
                pass  # Si la MIB ne charge pas correctement, on passe à la suivante

        raise Exception(f"Impossible de charger une MIB pour l'OID {oid}")


# Exemple avec un OID inconnu initialement
oid_test = ['1.3.6.1.2.1.105.1.1.1.3.1.1', '1.3.6.1.2.1.1.9.1.2.1']
for i in oid_test:
    try:
        label = load_mib_for_oid(i)
        print(f"OID résolu : {i} -> {label}")
    except Exception as e:
        print(e)
