# Lan Audacity

## Origine

Dans le cadre d'un projet d'Open Innovation, les élèves ont choisi de développer un outil permettant de gagner du temps pour le paramétrage des matériels réseaux (physiques et virtuels).

Les objectifs de "Lan Audacity" sont :
- Gagner du temps pour les techniciens réseaux
- Simplicité d'utilisation
- Polyvalence de l'outil
- Simplicité de paramétrage
- Gain de performances grâce à l’automatisation

## Description pour béotiens

Lan Audacity est un outil conçu pour simplifier et accélérer la configuration des équipements réseaux. Que vous soyez un débutant ou ayez peu d'expérience dans le domaine des réseaux, Lan Audacity vous permet de configurer vos appareils de manière rapide et efficace. Grâce à son interface intuitive, il rend les tâches complexes accessibles et faciles à réaliser pour tous.

Il utilise plusieurs protocoles Internet tels que :
- **ICMP (Internet Control Message Protocol)**
- **SNMP (Simple Network Management Protocol)**

Lan Audacity intègre trois types de vues pour une meilleure visualisation et gestion des réseaux :
1. **Vue cartographique physique** : Représente les équipements réseaux physiques avec une précision de 80 % par rapport à la réalité.
2. **Vue cartographique virtuelle** : Représente les réseaux virtuels avec une précision de 80 % par rapport à la réalité.
3. **Vue simple** : Offre une vue directe et simplifiée des réseaux.

De plus, Lan Audacity possède une capacité d'extension qui permet d'ajouter de nouvelles fonctionnalités selon les besoins, offrant ainsi une flexibilité et une évolutivité maximales pour répondre aux diverses exigences des utilisateurs.

## Description pour professionnels (Techniques)

Lan Audacity est un outil avancé de configuration réseau, conçu pour les techniciens et ingénieurs réseaux. Il supporte une large gamme d'équipements, tant physiques que virtuels, et est conçu pour automatiser de nombreuses tâches de paramétrage, augmentant ainsi l'efficacité et la productivité.

### Protocoles Supportés

Lan Audacity utilise plusieurs protocoles standard de l'industrie pour garantir une gestion et une configuration réseau optimales :
- **ICMP (Internet Control Message Protocol)** : Utilisé pour diagnostiquer les problèmes de réseau.
- **SNMP (Simple Network Management Protocol)** : Utilisé pour la surveillance et la gestion des équipements réseau.

### Vues Intégrées

Pour une gestion efficace, Lan Audacity propose trois types de vues :
1. **Vue cartographique physique** : Représente les équipements réseaux physiques avec une précision de 80 % par rapport à la réalité, facilitant ainsi la gestion des infrastructures matérielles.
2. **Vue cartographique virtuelle** : Représente les réseaux virtuels avec une précision de 80 % par rapport à la réalité, simplifiant la gestion des environnements virtualisés.
3. **Vue simple** : Offre une vue directe et simplifiée des réseaux, idéale pour un aperçu rapide et une gestion de base.

### Extensions et Flexibilité

Lan Audacity intègre une capacité à ajouter des extensions, permettant aux professionnels d'adapter et de personnaliser l'outil en fonction des besoins spécifiques de leurs infrastructures réseau. Cette modularité assure une évolutivité et une flexibilité maximales, répondant aux exigences changeantes des environnements réseau modernes.

### Fonctionnalités Avancées

- **Détection automatique des périphériques** : Identifie et configure automatiquement les équipements réseau.
- **Configuration en masse** : Permet de configurer plusieurs équipements simultanément, réduisant ainsi le temps de déploiement.
- **Outils de diagnostic avancés** : Fournit des outils robustes pour diagnostiquer et résoudre rapidement les problèmes réseau.

Les professionnels apprécieront la robustesse et la fiabilité de Lan Audacity, ainsi que la réduction significative du temps de configuration grâce à ses capacités d'automatisation et à son interface intuitive.

## Les outils pour Lan Audacity

**Lan Audacity** est un logiciel développé en Python. Le choix de Python s'explique par plusieurs raisons :

- **Accessibilité aux bibliothèques** : Python offre un accès facile à une multitude de bibliothèques, facilitant ainsi le développement de fonctionnalités complexes sans réinventer la roue.
- **Langage largement utilisé dans le domaine des réseaux** : Python est couramment utilisé pour les scripts de réseau, l'automatisation et la gestion des configurations, ce qui en fait un choix naturel pour ce type de projet.
- **Apprentissage et utilisation en cours** : Python est souvent enseigné dans les cursus informatiques, ce qui le rend familier aux étudiants et leur permet de contribuer efficacement au développement du logiciel.
- **Polyvalence** : Python est un langage polyvalent, capable de gérer des tâches variées allant du traitement des données à la gestion des systèmes, en passant par le développement web et l'automatisation.

En utilisant Python, Lan Audacity bénéficie de :

- **Simplicité et lisibilité du code** : Le code Python est connu pour sa clarté et sa facilité de lecture, ce qui facilite la maintenance et la collaboration entre les développeurs.
- **Communauté active et support** : Python possède une communauté active qui produit une abondante documentation et offre un support continu, ce qui est un atout majeur pour résoudre les problèmes et améliorer le logiciel.
- **Compatibilité multiplateforme** : Python fonctionne sur la plupart des systèmes d'exploitation, garantissant que Lan Audacity peut être utilisé sur différents environnements sans modification majeure du code.

Grâce à ces avantages, Python s'avère être le choix idéal pour le développement de Lan Audacity, assurant une efficacité optimale et une adaptabilité aux besoins évolutifs du projet.

### Bibliothèques Utilisées

Avec Python, nous utilisons plusieurs bibliothèques spécifiques pour optimiser les fonctionnalités de Lan Audacity. Voici une justification détaillée du choix de chaque bibliothèque utilisée :

#### PyYAML
- **Justification** : PyYAML est une bibliothèque puissante pour la lecture et l'écriture de fichiers YAML, qui sont souvent utilisés pour les fichiers de configuration en raison de leur simplicité et de leur lisibilité. En utilisant PyYAML, Lan Audacity peut facilement gérer et manipuler les configurations réseau, permettant une intégration transparente et une flexibilité dans la gestion des paramètres.
  
#### python-nmap
- **Justification** : La bibliothèque python-nmap permet d'utiliser l'outil Nmap directement depuis Python. Nmap est un outil de scan de réseau populaire et largement utilisé pour découvrir les hôtes et services sur un réseau. En intégrant python-nmap, Lan Audacity peut effectuer des scans de réseau avancés, détecter automatiquement les périphériques et obtenir des informations détaillées sur les équipements réseau.

#### pyasyncore
- **Justification** : Pyasyncore est une bibliothèque qui facilite le développement de fonctions asynchrones. L'utilisation de l'asynchronisme est cruciale pour gérer efficacement les opérations réseau non bloquantes et les tâches simultanées. Cela améliore la performance de Lan Audacity en permettant de traiter plusieurs requêtes et opérations de manière concurrente sans ralentir le système.

#### pysnmp
- **Justification** : pysnmp est une bibliothèque permettant d'utiliser le protocole SNMP (Simple Network Management Protocol). SNMP est essentiel pour la surveillance et la gestion des équipements réseau. En intégrant pysnmp, Lan Audacity peut surveiller les performances du réseau, collecter des données et envoyer des alertes en cas de problèmes, offrant ainsi une gestion proactive et efficace des réseaux.

#### PyQt5 / PyQt6
- **Justification** : PyQt5 et PyQt6 sont des bibliothèques utilisées pour créer des interfaces utilisateur graphiques (GUI) en Python. Elles sont basées sur le framework Qt, connu pour sa robustesse et sa flexibilité. En utilisant PyQt, Lan Audacity peut offrir une interface utilisateur intuitive et interactive, rendant l'outil accessible et facile à utiliser pour les utilisateurs, qu'ils soient débutants ou professionnels.

En combinant ces bibliothèques, Lan Audacity bénéficie d'une base technologique solide, assurant des fonctionnalités avancées, une performance optimale et une expérience utilisateur améliorée.