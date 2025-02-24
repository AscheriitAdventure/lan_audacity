-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost
-- Généré le : mar. 08 oct. 2024 à 14:13
-- Version du serveur : 5.7.11
-- Version de PHP : 8.3.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `lan_audacity_sql_server`
--

-- --------------------------------------------------------

--
-- Structure de la table `clockmanager`
--

CREATE TABLE `clockmanager` (
  `clock_manager_id` int(10) UNSIGNED NOT NULL,
  `created_at` float NOT NULL,
  `updated_at` float NOT NULL,
  `type_time` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `device`
--

CREATE TABLE `device` (
  `device_id` int(10) UNSIGNED NOT NULL,
  `uuid` char(36) NOT NULL,
  `name_object` varchar(100) DEFAULT 'Unknown',
  `web_address_id` int(10) UNSIGNED DEFAULT NULL,
  `clock_manager_id` int(10) UNSIGNED DEFAULT NULL,
  `type_device_id` int(10) UNSIGNED DEFAULT NULL,
  `vendor` varchar(100) DEFAULT NULL,
  `mac_address` varchar(17) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `devicesubdevice`
--

CREATE TABLE `devicesubdevice` (
  `parent_device_id` int(10) UNSIGNED NOT NULL,
  `sub_device_id` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `devicetype`
--

CREATE TABLE `devicetype` (
  `device_type_id` int(10) UNSIGNED NOT NULL,
  `pixmap_path` varchar(255) DEFAULT NULL,
  `osi_layer_id` int(10) UNSIGNED DEFAULT NULL,
  `category_description` text,
  `category_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `devicetype`
--

INSERT INTO `devicetype` (`device_type_id`, `pixmap_path`, `osi_layer_id`, `category_description`, `category_name`) VALUES
(1, NULL, 7, 'This category contains general-purpose operating systems like Linux and Windows. In the nmap-service-probes file this class is indicated by a lack of a d// field.', 'general purpose'),
(2, NULL, 2, 'A bridge combines two or more subnetworks into one. With a bridge this happens at a lower level than with a router. This category also includes things like Ethernet-to-serial bridges.', 'bridge'),
(3, NULL, 3, 'Devices in this category connect a network to the Internet via cable, ADSL, fiber optics, etc. Some of these devices provide network address translation, a firewall, port forwarding, or other services.', 'broadband router'),
(4, NULL, 4, "A firewall controls what traffic is allowed into or out of a network. Some also have additional capabilities. This category doesn\'t include general-purpose operating systems that happen to come with a firewall, but it does include OS distributions purpose-built to work only as a firewall.", 'firewall'),
(5, NULL, 7, 'A video game console like the Xbox or PlayStation.', 'game console'),
(6, NULL, 2, 'A hub joins network segments by re-broadcasting all traffic. Hubs are distinct from switches, which selectively transmit packets only to relevant destinations.', 'hub'),
(7, NULL, 4, 'A device that distributes inbound traffic to multiple devices to ease the load on those devices.', 'load balancer'),
(8, NULL, 7, 'This category includes all kinds of audiovisual equipment, including portable music players, home audio systems, TVs, and projectors.', 'media device'),
(9, NULL, 7, 'A private branch exchange, or PBX, routes telephone calls within a private organization and connects them to the public telephone network or VoIP.', 'PBX'),
(10, NULL, 7, "A handheld computer. Devices that are also telephones go in the \'phone\' category.", 'PDA'),
(11, NULL, 7, 'A network-capable telephone that is not a VoIP phone. Devices in this category are typically mobile phones.', 'phone'),
(12, NULL, 7, 'Miscellaneous power devices like uninterruptable power supplies and surge protectors.', 'power-device'),
(13, NULL, 7, 'Network-enabled printers, including printers with an embedded print server.', 'printer'),
(14, NULL, 7, "A print server connects a printer to a network. Printers that contain their own print server go in the \'printer\' category instead.", 'print server'),
(15, NULL, 7, 'Any kind of proxy, including web proxies and other servers that cache data or understand high-level protocols.', 'proxy server'),
(16, NULL, 7, 'Devices that allow servers or other equipment to be monitored or managed remotely.', 'remote management'),
(17, NULL, 3, 'Routers connect multiple networks. They are distinct from hubs and switches because they route packets between different networks as opposed to extending one network.', 'router'),
(18, NULL, 7, "Any security device that doesn\'t fall into the “firewall” category belongs in this category. This includes intrusion detection and prevention systems.", 'security-misc'),
(19, NULL, 7, "The catch-all category. If a device doesn\'t fall into one of the other categories, it is specialized. Examples in this category are diverse and include such things as clocks, oscilloscopes, climate sensors, and more.", 'specialized'),
(20, NULL, 7, 'Data storage devices like tape decks and network-attached storage appliances.', 'storage-misc'),
(21, NULL, 2, 'A device that extends a network by selectively re-broadcasting packets. Switches are distinct from hubs, which broadcast all packets.', 'switch'),
(22, NULL, 7, "Devices used by telephone systems that aren\'t PBXs, like voicemail and ISDN systems.", 'telecom-misc'),
(23, NULL, 7, 'A device with a keyboard and monitor with the primary purpose of communicating directly with a terminal server or mainframe.', 'terminal'),
(24, NULL, 7, 'A device providing terminal facilities to clients over a network.', 'terminal server'),
(25, NULL, 7, 'A device that converts between voice over IP (VoIP) protocols and normal telephone traffic. Also may convert different VoIP protocols.', 'VoIP adapter'),
(26, NULL, 7, 'A phone capable of a VoIP protocol.', 'VoIP phone'),
(27, NULL, 2, 'Wireless access points offer a wireless connection to a network. Most work with radio technology like 802.11b but some use infra-red or something else. Devices that could also be put in another category, like wireless broadband routers, are put in the WAP category because WAPs require special network considerations.', 'WAP'),
(28, NULL, 7, 'Any kind of camera that stores or transmits pictures or video. This includes everything from consumer webcams to security system cameras.', 'webcam');

-- --------------------------------------------------------

--
-- Structure de la table `network`
--

CREATE TABLE `network` (
  `network_id` int(10) UNSIGNED NOT NULL,
  `uuid` char(36) NOT NULL,
  `name_object` varchar(100) DEFAULT 'Unknown',
  `web_address_id` int(10) UNSIGNED DEFAULT NULL,
  `clock_manager_id` int(10) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `networkdevice`
--

CREATE TABLE `networkdevice` (
  `network_id` int(10) UNSIGNED NOT NULL,
  `device_id` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `osaccuracy`
--

CREATE TABLE `osaccuracy` (
  `os_accuracy_id` int(10) UNSIGNED NOT NULL,
  `name_object` varchar(100) NOT NULL,
  `accuracy_int` int(10) UNSIGNED DEFAULT NULL,
  `device_id` int(10) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `osilayer`
--

CREATE TABLE `osilayer` (
  `osi_layer_id` int(10) UNSIGNED NOT NULL,
  `layer_name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `osilayer`
--

INSERT INTO `osilayer` (`osi_layer_id`, `layer_name`) VALUES
(1, 'PHYSICAL'),
(2, 'DATA_LINK'),
(3, 'NETWORK'),
(4, 'TRANSPORT'),
(5, 'SESSION'),
(6, 'PRESENTATION'),
(7, 'APPLICATION');

-- --------------------------------------------------------

--
-- Structure de la table `portsobject`
--

CREATE TABLE `portsobject` (
  `port_id` int(10) UNSIGNED NOT NULL,
  `port_number` int(10) UNSIGNED DEFAULT NULL,
  `protocol` varchar(15) DEFAULT 'NON Renseigné',
  `port_status` varchar(30) DEFAULT 'NON Renseigné',
  `port_service` varchar(255) DEFAULT 'NON Renseigné',
  `port_version` varchar(255) DEFAULT 'NON Renseigné',
  `device_id` int(10) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `updateatlist`
--

CREATE TABLE `updateatlist` (
  `update_at_id` int(10) UNSIGNED NOT NULL,
  `clock_manager_id` int(10) UNSIGNED DEFAULT NULL,
  `update_at` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `webaddress`
--

CREATE TABLE `webaddress` (
  `web_address_id` int(10) UNSIGNED NOT NULL,
  `ipv4` varchar(15) DEFAULT NULL,
  `mask_ipv4` varchar(15) DEFAULT NULL,
  `ipv4_public` varchar(15) DEFAULT NULL,
  `cidr` varchar(18) DEFAULT NULL,
  `ipv6_local` varchar(45) DEFAULT NULL,
  `ipv6_global` varchar(45) DEFAULT NULL,
  `domain_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `clockmanager`
--
ALTER TABLE `clockmanager`
  ADD PRIMARY KEY (`clock_manager_id`);

--
-- Index pour la table `device`
--
ALTER TABLE `device`
  ADD PRIMARY KEY (`device_id`),
  ADD KEY `web_address_id` (`web_address_id`),
  ADD KEY `clock_manager_id` (`clock_manager_id`),
  ADD KEY `type_device_id` (`type_device_id`);

--
-- Index pour la table `devicesubdevice`
--
ALTER TABLE `devicesubdevice`
  ADD PRIMARY KEY (`parent_device_id`,`sub_device_id`),
  ADD KEY `sub_device_id` (`sub_device_id`);

--
-- Index pour la table `devicetype`
--
ALTER TABLE `devicetype`
  ADD PRIMARY KEY (`device_type_id`),
  ADD KEY `osi_layer_id` (`osi_layer_id`);

--
-- Index pour la table `network`
--
ALTER TABLE `network`
  ADD PRIMARY KEY (`network_id`),
  ADD KEY `web_address_id` (`web_address_id`),
  ADD KEY `clock_manager_id` (`clock_manager_id`);

--
-- Index pour la table `networkdevice`
--
ALTER TABLE `networkdevice`
  ADD PRIMARY KEY (`network_id`,`device_id`),
  ADD KEY `device_id` (`device_id`);

--
-- Index pour la table `osaccuracy`
--
ALTER TABLE `osaccuracy`
  ADD PRIMARY KEY (`os_accuracy_id`),
  ADD KEY `device_id` (`device_id`);

--
-- Index pour la table `osilayer`
--
ALTER TABLE `osilayer`
  ADD PRIMARY KEY (`osi_layer_id`);

--
-- Index pour la table `portsobject`
--
ALTER TABLE `portsobject`
  ADD PRIMARY KEY (`port_id`),
  ADD KEY `device_id` (`device_id`);

--
-- Index pour la table `updateatlist`
--
ALTER TABLE `updateatlist`
  ADD PRIMARY KEY (`update_at_id`),
  ADD KEY `clock_manager_id` (`clock_manager_id`);

--
-- Index pour la table `webaddress`
--
ALTER TABLE `webaddress`
  ADD PRIMARY KEY (`web_address_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `clockmanager`
--
ALTER TABLE `clockmanager`
  MODIFY `clock_manager_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `device`
--
ALTER TABLE `device`
  MODIFY `device_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `devicetype`
--
ALTER TABLE `devicetype`
  MODIFY `device_type_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT pour la table `network`
--
ALTER TABLE `network`
  MODIFY `network_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `osaccuracy`
--
ALTER TABLE `osaccuracy`
  MODIFY `os_accuracy_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `portsobject`
--
ALTER TABLE `portsobject`
  MODIFY `port_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `updateatlist`
--
ALTER TABLE `updateatlist`
  MODIFY `update_at_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `webaddress`
--
ALTER TABLE `webaddress`
  MODIFY `web_address_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `device`
--
ALTER TABLE `device`
  ADD CONSTRAINT `device_ibfk_1` FOREIGN KEY (`web_address_id`) REFERENCES `webaddress` (`web_address_id`) ON DELETE SET NULL,
  ADD CONSTRAINT `device_ibfk_2` FOREIGN KEY (`clock_manager_id`) REFERENCES `clockmanager` (`clock_manager_id`) ON DELETE SET NULL,
  ADD CONSTRAINT `device_ibfk_3` FOREIGN KEY (`type_device_id`) REFERENCES `devicetype` (`device_type_id`) ON DELETE SET NULL;

--
-- Contraintes pour la table `devicesubdevice`
--
ALTER TABLE `devicesubdevice`
  ADD CONSTRAINT `devicesubdevice_ibfk_1` FOREIGN KEY (`parent_device_id`) REFERENCES `devicetype` (`device_type_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `devicesubdevice_ibfk_2` FOREIGN KEY (`sub_device_id`) REFERENCES `devicetype` (`device_type_id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `devicetype`
--
ALTER TABLE `devicetype`
  ADD CONSTRAINT `devicetype_ibfk_1` FOREIGN KEY (`osi_layer_id`) REFERENCES `osilayer` (`osi_layer_id`) ON DELETE SET NULL;

--
-- Contraintes pour la table `network`
--
ALTER TABLE `network`
  ADD CONSTRAINT `network_ibfk_1` FOREIGN KEY (`web_address_id`) REFERENCES `webaddress` (`web_address_id`) ON DELETE SET NULL,
  ADD CONSTRAINT `network_ibfk_2` FOREIGN KEY (`clock_manager_id`) REFERENCES `clockmanager` (`clock_manager_id`) ON DELETE SET NULL;

--
-- Contraintes pour la table `networkdevice`
--
ALTER TABLE `networkdevice`
  ADD CONSTRAINT `networkdevice_ibfk_1` FOREIGN KEY (`network_id`) REFERENCES `network` (`network_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `networkdevice_ibfk_2` FOREIGN KEY (`device_id`) REFERENCES `device` (`device_id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `osaccuracy`
--
ALTER TABLE `osaccuracy`
  ADD CONSTRAINT `osaccuracy_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `device` (`device_id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `portsobject`
--
ALTER TABLE `portsobject`
  ADD CONSTRAINT `portsobject_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `device` (`device_id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `updateatlist`
--
ALTER TABLE `updateatlist`
  ADD CONSTRAINT `updateatlist_ibfk_1` FOREIGN KEY (`clock_manager_id`) REFERENCES `clockmanager` (`clock_manager_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
