CREATE DATABASE IF NOT EXISTS lan_audacity_sql_server 
DEFAULT CHARACTER SET utf8 
COLLATE utf8_general_ci;

USE lan_audacity_sql_server;

/* Table structure for table `ClockManager` */
CREATE TABLE IF NOT EXISTS ClockManager (
    clock_manager_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    created_at FLOAT NOT NULL,
    updated_at FLOAT NOT NULL,
    type_time VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS UpdateAtList (
    update_at_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    clock_manager_id INT UNSIGNED,
    update_at FLOAT NOT NULL,
    FOREIGN KEY (clock_manager_id) REFERENCES ClockManager(clock_manager_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table structure for table `OSILayer` */
CREATE TABLE IF NOT EXISTS OSILayer (
    osi_layer_id INT UNSIGNED PRIMARY KEY,
    layer_name VARCHAR(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO OSILayer (osi_layer_id, layer_name) VALUES
(1, 'PHYSICAL'),
(2, 'DATA_LINK'),
(3, 'NETWORK'),
(4, 'TRANSPORT'),
(5, 'SESSION'),
(6, 'PRESENTATION'),
(7, 'APPLICATION');

/* Table structure for table `DeviceType` */
CREATE TABLE IF NOT EXISTS DeviceType (
    device_type_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,  -- Identifiant unique pour chaque DeviceType
    pixmap_path VARCHAR(255),  -- Chemin de l'image (le type str est traduit en VARCHAR)
    osi_layer_id INT UNSIGNED,  -- Référence vers la table OSILayer
    category_description TEXT,  -- Description de la catégorie
    category_name VARCHAR(100) NOT NULL,  -- Nom de la catégorie
    FOREIGN KEY (osi_layer_id) REFERENCES OSILayer(osi_layer_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS DeviceSubDevice (
    parent_device_id INT UNSIGNED,  -- Le périphérique parent
    sub_device_id INT UNSIGNED,     -- Le sous-périphérique
    PRIMARY KEY (parent_device_id, sub_device_id),  -- Clé primaire combinée
    FOREIGN KEY (parent_device_id) REFERENCES DeviceType(device_type_id) ON DELETE CASCADE,  -- Relation vers DeviceType
    FOREIGN KEY (sub_device_id) REFERENCES DeviceType(device_type_id) ON DELETE CASCADE      -- Relation vers DeviceType
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table structure for `NetworkObjects` */
CREATE TABLE IF NOT EXISTS WebAddress (
    web_address_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,  -- Identifiant unique pour chaque entrée WebAddress
    ipv4 VARCHAR(15),      -- Adresse IPv4, max 15 caractères (xxx.xxx.xxx.xxx)
    mask_ipv4 VARCHAR(15), -- Masque de sous-réseau IPv4, format similaire à IPv4
    ipv4_public VARCHAR(15), -- Adresse IPv4 publique, format similaire à IPv4
    cidr VARCHAR(18),      -- Représentation CIDR (ex: 192.168.0.0/24)
    ipv6_local VARCHAR(45), -- Adresse IPv6 locale, max 45 caractères
    ipv6_global VARCHAR(45) -- Adresse IPv6 globale, max 45 caractères
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table structure for table `Device` */
CREATE TABLE IF NOT EXISTS Device (
    device_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,  -- Identifiant unique pour chaque périphérique
    uuid CHAR(36) NOT NULL,                             -- UUID, format 36 caractères
    name_object VARCHAR(100) DEFAULT 'Unknown',         -- Nom du périphérique, par défaut 'Unknown'
    web_address_id INT UNSIGNED,                        -- Clé étrangère vers la table WebAddress
    clock_manager_id INT UNSIGNED,                      -- Clé étrangère vers la table ClockManager
    type_device_id INT UNSIGNED,                        -- Clé étrangère vers la table DeviceType
    vendor VARCHAR(100),                                -- Fabricant du périphérique
    mac_address VARCHAR(17),                            -- Adresse MAC, format 'XX:XX:XX:XX:XX:XX'
    FOREIGN KEY (web_address_id) REFERENCES WebAddress(web_address_id) ON DELETE SET NULL,  -- Relation avec WebAddress
    FOREIGN KEY (clock_manager_id) REFERENCES ClockManager(clock_manager_id) ON DELETE SET NULL,  -- Relation avec ClockManager
    FOREIGN KEY (type_device_id) REFERENCES DeviceType(device_type_id) ON DELETE SET NULL  -- Relation avec DeviceType
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table structure for table `Network` */
CREATE TABLE IF NOT EXISTS Network (
    network_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,   -- Identifiant unique pour chaque réseau
    uuid CHAR(36) NOT NULL,                               -- UUID, format 36 caractères
    name_object VARCHAR(100) DEFAULT 'Unknown',           -- Nom du réseau, par défaut 'Unknown'
    web_address_id INT UNSIGNED,                          -- Clé étrangère vers la table WebAddress
    clock_manager_id INT UNSIGNED,                        -- Clé étrangère vers la table ClockManager
    dns_object VARCHAR(255),                              -- Objet DNS (par exemple : nom de domaine)
    FOREIGN KEY (web_address_id) REFERENCES WebAddress(web_address_id) ON DELETE SET NULL,  -- Relation avec WebAddress
    FOREIGN KEY (clock_manager_id) REFERENCES ClockManager(clock_manager_id) ON DELETE SET NULL  -- Relation avec ClockManager
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS NetworkDevice (
    network_id INT UNSIGNED,      -- Clé étrangère vers la table Network
    device_id INT UNSIGNED,       -- Clé étrangère vers la table Device
    PRIMARY KEY (network_id, device_id),   -- Clé primaire combinée pour éviter les doublons
    FOREIGN KEY (network_id) REFERENCES Network(network_id) ON DELETE CASCADE,  -- Relation vers Network
    FOREIGN KEY (device_id) REFERENCES Device(device_id) ON DELETE CASCADE      -- Relation vers Device
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS OSAccuracy (
    os_accuracy_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,  -- Identifiant unique pour chaque entrée OSAccuracy
    name_object VARCHAR(100) NOT NULL,                       -- Nom de la précision
    accuracy_int INT UNSIGNED,                               -- Valeur de la précision
    device_id INT UNSIGNED,                                  -- Clé étrangère vers la table Device
    FOREIGN KEY (device_id) REFERENCES Device(device_id) ON DELETE CASCADE  -- Relation vers Device
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS PortsObject (
    port_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,   -- Identifiant unique pour chaque entrée PortsObject
    port_number INT UNSIGNED,                          -- Numéro de port
    protocol VARCHAR(15) DEFAULT 'NON Renseigné',      -- Protocole utilisé
    port_status VARCHAR(30) DEFAULT 'NON Renseigné',   -- État du port
    port_service VARCHAR(255) DEFAULT 'NON Renseigné', -- Nom du service
    port_version VARCHAR(255) DEFAULT 'NON Renseigné', -- Version du port
    device_id INT UNSIGNED,                            -- Clé étrangère vers la table Device
    FOREIGN KEY (device_id) REFERENCES Device(device_id) ON DELETE CASCADE  -- Relation vers Device
) ENGINE=InnoDB DEFAULT CHARSET=utf8;