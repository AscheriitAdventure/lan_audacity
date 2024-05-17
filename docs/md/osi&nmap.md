# Nmap
link: [Nmap](nmap.org)

## Book: Device Type
### Table (Translate: English to French)
Voici un tableau représentant les catégories mentionnées avec leurs descriptions :

|Couche OSI|Catégorie| Description|
|:--:|:---|:---|
|7|`general purpose`|Systèmes d'exploitation généraux tels que Linux et Windows. Cette catégorie est indiquée par l'absence de champ d// dans le fichier nmap-service-probes.|
|2|`bridge`|Un pont combine deux ou plusieurs sous-réseaux en un seul. Avec un pont, cela se produit à un niveau inférieur qu'avec un routeur. Cette catégorie inclut également des éléments comme les ponts Ethernet-to-serial.|
|3|`broadband router`|Les appareils de cette catégorie connectent un réseau à Internet via le câble, l'ADSL, la fibre optique, etc. Certains de ces appareils fournissent une traduction d'adresse réseau, un pare-feu, un transfert de port ou d'autres services.|
|4|`firewall`|Un pare-feu contrôle quel trafic est autorisé dans ou hors d'un réseau. Certains ont également des capacités supplémentaires. Cette catégorie n'inclut pas les systèmes d'exploitation généraux qui incluent un pare-feu, mais elle inclut les distributions d'OS construites uniquement pour fonctionner uniquement comme pare-feu.|
|7|`game console`|Une console de jeu vidéo comme la Xbox ou la PlayStation.|
|1|`hub`|Un concentrateur relie des segments de réseau en rebroadcastant tout le trafic. Les hubs sont distincts des commutateurs, qui transmettent sélectivement les paquets uniquement vers les destinations pertinentes.|
|4|`load balancer`|Un appareil qui distribue le trafic entrant à plusieurs appareils pour soulager la charge sur ces appareils.|
|7|`media device`|Cette catégorie inclut toutes sortes d'équipements audiovisuels, y compris les lecteurs de musique portables, les systèmes audio domestiques, les téléviseurs et les projecteurs.|
|7|`PBX`|Private Branch Exchange:<br>Un autocommutateur privé, ou PBX, route les appels téléphoniques à l'intérieur d'une organisation privée et les connecte au réseau téléphonique public ou à la VoIP.|
|7|`PDA`|Personal Digital Assistant:<br>Un ordinateur de poche. Les appareils qui sont également des téléphones vont dans la catégorie "téléphone".|
|7|`phone`| Un téléphone réseau capable qui n'est pas un téléphone VoIP. Les appareils de cette catégorie sont généralement des téléphones mobiles.|
|7|`power-device`|Divers dispositifs d'alimentation tels que les alimentations sans coupure et les parasurtenseurs.|
|7|`printer`|Imprimantes réseau, y compris les imprimantes avec un serveur d'impression intégré.|
|7|`print server`|Un serveur d'impression connecte une imprimante à un réseau. Les imprimantes qui contiennent leur propre serveur d'impression vont dans la catégorie "imprimante" au lieu de cela.|
|7|`proxy server`|Tout type de proxy, y compris les proxies Web et autres serveurs qui mettent en cache des données ou comprennent des protocoles de haut niveau.|
|7|`remote management`|Des dispositifs qui permettent de surveiller ou de gérer à distance des serveurs ou d'autres équipements.|
|3|`router`|Les routeurs connectent plusieurs réseaux. Ils sont distincts des concentrateurs et des commutateurs car ils routent les paquets entre différents réseaux au lieu d'étendre un réseau.|
|7|`security-misc`|Tout dispositif de sécurité qui ne rentre pas dans la catégorie "pare-feu" appartient à cette catégorie. Cela inclut la détection et la prévention des intrusions.|
|7|`specialized`|La catégorie fourre-tout. Si un appareil ne rentre dans aucune des autres catégories, il est spécialisé. Les exemples dans cette catégorie sont divers et comprennent des choses comme les horloges, les oscilloscopes, les capteurs climatiques, et plus encore.|
|7|`storage-misc`|Des dispositifs de stockage de données comme les lecteurs de bandes et les appareils de stockage en réseau.|
|2|`switch`|Un appareil qui étend un réseau en retransmettant sélectivement les paquets. Les commutateurs sont distincts des concentrateurs, qui diffusent tous les paquets.|
|7|`telecom-misc`|Des dispositifs utilisés par les systèmes téléphoniques qui ne sont pas des PBX, comme la messagerie vocale et les systèmes ISDN.|
|7|`terminal`|Un appareil avec un clavier et un écran ayant pour but principal de communiquer directement avec un serveur de terminaux ou un ordinateur central.|
|7|`terminal server`|Un appareil fournissant des installations de terminaux à des clients sur un réseau.|
|7|`VoIP adapter`|Un appareil qui convertit entre les protocoles de voix sur IP (VoIP) et le trafic téléphonique normal.|
|7|`VoIP phone`|Un téléphone capable d'un protocole VoIP.|
|3|`WAP`|Wireless Access Point:<br>Les points d'accès sans fil offrent une connexion sans fil à un réseau. La plupart fonctionnent avec une technologie radio comme le 802.11b, mais certains utilisent des infrarouges ou autre chose. Les appareils qui pourraient également être mis dans une autre catégorie, comme les routeurs haut débit sans fil, sont mis dans la catégorie WAP car les WAP nécessitent des considérations réseau spéciales.|
|7|`webcam`|Tout type de caméra qui stocke ou transmet des images ou des vidéos. Cela inclut tout, des webcams grand public aux caméras de système de sécurité.|

# Personel
## Book: Device Type
Voici la colonne "Description" complétée :

| Couche OSI | Catégorie| Description|
|:--:|:---|:---|
|1|`optic fiber`|Utilise des fibres optiques pour transmettre des données à travers des signaux lumineux.|
|1|`ethernet/rj45`|Utilise des câbles Ethernet et des connecteurs RJ45 pour transmettre des données sur un réseau local.|
|2|`network card`|Carte réseau installée dans un ordinateur pour permettre la communication avec d'autres appareils sur un réseau.|
|2|`modem`|Convertit les signaux numériques d'un ordinateur en signaux analogiques pour la transmission sur un réseau de données analogiques.|
|2|`switch l2/l2+`|Un commutateur de couche 2 (L2) ou de couche 2+ (L2+) agit comme un pont intelligent, transmettant des trames en fonction des adresses MAC.|
|2|`switch l3`|Un commutateur de couche 3 (L3) fonctionne au niveau du réseau et utilise des adresses IP pour acheminer le trafic entre différents réseaux.|
|3|`wifi router`|Un routeur WiFi permet de connecter plusieurs appareils à un réseau local sans fil (WiFi) et de les relier à Internet.|
|7|`server`|Un serveur est un appareil ou un logiciel qui fournit des fonctionnalités ou des services à d'autres appareils, souvent dans le cadre d'un réseau informatique.|