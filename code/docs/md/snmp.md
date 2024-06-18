# SNMP

## OID

### Définition
L'Object Identifier (OID) est un identifiant unique utilisé dans le protocole SNMP (Simple Network Management Protocol) pour désigner un objet spécifique dans une MIB (Management Information Base). Chaque OID représente une variable spécifique qui peut être surveillée ou contrôlée sur un appareil réseau, comme un routeur, un commutateur, une imprimante, ou tout autre dispositif compatible SNMP. Les OIDs sont essentiels pour la gestion des réseaux, car ils permettent aux administrateurs de collecter des informations, de configurer des paramètres et de surveiller les performances des appareils.

## MIB

### Définition
MIB, acronyme de "Management Information Base" (Base d'Informations de Gestion), est une base de données utilisée pour la gestion des réseaux. Elle est essentielle pour les protocoles de gestion de réseau, comme SNMP (Simple Network Management Protocol). Une MIB contient des informations organisées en un ensemble hiérarchique de données concernant les objets gérés dans un réseau. Ces objets peuvent être des dispositifs tels que des routeurs, des commutateurs, des serveurs, et d'autres équipements réseau. Chaque objet dans la MIB est identifié par un identifiant unique appelé OID (Object Identifier).

### Structure
La structure d'une MIB est hiérarchique et ressemble à un arbre, où chaque nœud représente un objet géré. Les niveaux de cet arbre représentent des catégories de ces objets. La racine de cet arbre est universelle et partagée par toutes les MIB. Les branches suivantes se spécialisent pour différentes organisations, équipements et protocoles spécifiques. Voici une description détaillée des composants de cette structure :

1. **Nœuds Racine (Root Nodes) :** 
   - La racine de la hiérarchie MIB est généralement désignée par un nœud appelé "iso" (1).
   - Sous la racine, il y a des branches principales comme "org" (3) pour les organisations, "dod" (6) pour le Département de la Défense des États-Unis, et ainsi de suite.

2. **Nœuds Intermédiaires :**
   - Les nœuds intermédiaires divisent les branches principales en sous-branches plus spécifiques. Par exemple, sous "dod" (6), on trouve "internet" (1).
   - Chaque sous-branche représente une catégorie plus spécifique de gestion réseau ou de standards.

3. **Feuilles (Leaves) :**
   - Les nœuds terminaux ou feuilles sont les objets gérés spécifiques. Ces nœuds contiennent des informations détaillées et des données de gestion comme le type de données, les limites acceptables, et les actions possibles.
   - Chaque feuille est définie par un OID unique, par exemple, l'OID 1.3.6.1.2.1.1.1 représente "sysDescr" qui est la description du système.

4. **Descriptions des Objets :**
   - Chaque objet ou nœud est décrit par des attributs comme le nom, le type de données (entier, chaîne, adresse IP, etc.), et les contraintes possibles (comme les valeurs minimum et maximum).
   - Les descriptions des objets sont spécifiées dans des documents appelés "Modules MIB", qui sont écrits dans un langage de définition standardisé, souvent en ASN.1 (Abstract Syntax Notation One).

5. **Modules MIB :**
   - Un module MIB est un fichier qui décrit un ensemble de nœuds (objets) et leurs relations. Ces modules peuvent être spécifiques à un fabricant, à un protocole, ou à un type de dispositif.
   - Les modules sont souvent partagés et publiés par des organisations telles que l'IETF (Internet Engineering Task Force), et peuvent être étendus pour inclure des informations spécifiques à des équipements particuliers.

En résumé, une MIB fournit une structure organisée et standardisée pour la gestion des informations réseau, facilitant ainsi la surveillance, le contrôle et l'administration des équipements et des services réseau à travers des outils de gestion comme SNMP.

## Bibliothèques python
### Bibliothèque snmp
### Bibliothèque oid
### Bibliothèque mib