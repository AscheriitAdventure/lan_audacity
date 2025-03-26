USE db_lanAudacity;

/* Table structure for `NetworkObjects` */
CREATE TABLE IF NOT EXISTS WebAddress (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,  -- Identifiant unique pour chaque entrée WebAddress
    ipv4 VARCHAR(15),      -- Adresse IPv4, max 15 caractères (xxx.xxx.xxx.xxx)
    mask_ipv4 VARCHAR(15), -- Masque de sous-réseau IPv4, format similaire à IPv4
    ipv4_public VARCHAR(15), -- Adresse IPv4 publique, format similaire à IPv4
    cidr VARCHAR(18),      -- Représentation CIDR (ex: 192.168.0.0/24)
    ipv6_local VARCHAR(45), -- Adresse IPv6 locale, max 45 caractères
    ipv6_global VARCHAR(45) -- Adresse IPv6 globale, max 45 caractères
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table structure for table `Device` */
CREATE TABLE IF NOT EXISTS Device (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,  -- Identifiant unique pour chaque périphérique
    uuid CHAR(36) NOT NULL,                             -- UUID, format 36 caractères
    name_object VARCHAR(100) DEFAULT 'Unknown',         -- Nom du périphérique, par défaut 'Unknown'
    web_address_id INT UNSIGNED,                        -- Clé étrangère vers la table WebAddress
    clock_manager_id INT UNSIGNED,                      -- Clé étrangère vers la table ClockManager
    type_device_id INT UNSIGNED,                        -- Clé étrangère vers la table DeviceType
    vendor VARCHAR(100),                                -- Fabricant du périphérique
    mac_address VARCHAR(17),                            -- Adresse MAC, format 'XX:XX:XX:XX:XX:XX'
    FOREIGN KEY (web_address_id) REFERENCES WebAddress(id) ON DELETE SET NULL,  -- Relation avec WebAddress
    FOREIGN KEY (clock_manager_id) REFERENCES ClockManager(id) ON DELETE SET NULL,  -- Relation avec ClockManager
    FOREIGN KEY (type_device_id) REFERENCES DeviceType(id) ON DELETE SET NULL  -- Relation avec DeviceType
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table structure for table `Network` */
CREATE TABLE IF NOT EXISTS Network (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,   -- Identifiant unique pour chaque réseau
    uuid CHAR(36) NOT NULL,                               -- UUID, format 36 caractères
    name_object VARCHAR(100) DEFAULT 'Unknown',           -- Nom du réseau, par défaut 'Unknown'
    web_address_id INT UNSIGNED,                          -- Clé étrangère vers la table WebAddress
    clock_manager_id INT UNSIGNED,                        -- Clé étrangère vers la table ClockManager
    domain_name VARCHAR(255),                              -- Objet DNS (par exemple : nom de domaine)
    FOREIGN KEY (web_address_id) REFERENCES WebAddress(id) ON DELETE SET NULL,  -- Relation avec WebAddress
    FOREIGN KEY (clock_manager_id) REFERENCES ClockManager(id) ON DELETE SET NULL  -- Relation avec ClockManager
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS NetworkDevice (
    network_id INT UNSIGNED,      -- Clé étrangère vers la table Network
    device_id INT UNSIGNED,       -- Clé étrangère vers la table Device
    PRIMARY KEY (network_id, device_id),   -- Clé primaire combinée pour éviter les doublons
    FOREIGN KEY (network_id) REFERENCES Network(id) ON DELETE CASCADE,  -- Relation vers Network
    FOREIGN KEY (device_id) REFERENCES Device(id) ON DELETE CASCADE      -- Relation vers Device
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS OSAccuracy (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,  -- Identifiant unique pour chaque entrée OSAccuracy
    name_object VARCHAR(100) NOT NULL,                       -- Nom de la précision
    accuracy_int INT UNSIGNED,                               -- Valeur de la précision
    device_id INT UNSIGNED,                                  -- Clé étrangère vers la table Device
    FOREIGN KEY (device_id) REFERENCES Device(id) ON DELETE CASCADE  -- Relation vers Device
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS PortsObject (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,   -- Identifiant unique pour chaque entrée PortsObject
    port_number INT UNSIGNED,                          -- Numéro de port
    protocol VARCHAR(15) DEFAULT 'NON Renseigné',      -- Protocole utilisé
    port_status VARCHAR(30) DEFAULT 'NON Renseigné',   -- État du port
    port_service VARCHAR(255) DEFAULT 'NON Renseigné', -- Nom du service
    port_version VARCHAR(255) DEFAULT 'NON Renseigné', -- Version du port
    device_id INT UNSIGNED,                            -- Clé étrangère vers la table Device
    FOREIGN KEY (device_id) REFERENCES Device(id) ON DELETE CASCADE  -- Relation vers Device
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS ProjectNetwork(
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    lan_audacity_id INT UNSIGNED NOT NULL,
    network_id INT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lan_audacity_id) REFERENCES LanAudacity(id),
    FOREIGN KEY (network_id) REFERENCES Network(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;