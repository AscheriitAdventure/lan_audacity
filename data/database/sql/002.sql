USE db_lanAudacity;


/* Table structure for table `OSILayer` */
CREATE TABLE IF NOT EXISTS OSILayer (
    id INT UNSIGNED PRIMARY KEY,
    layer_name VARCHAR(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO OSILayer (id, layer_name) VALUES
(1, 'PHYSICAL'),
(2, 'DATA_LINK'),
(3, 'NETWORK'),
(4, 'TRANSPORT'),
(5, 'SESSION'),
(6, 'PRESENTATION'),
(7, 'APPLICATION');

/* Table structure for table `DeviceType` */
CREATE TABLE IF NOT EXISTS DeviceType (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,  -- Identifiant unique pour chaque DeviceType
    pixmap_path VARCHAR(255),  -- Chemin de l'image (le type str est traduit en VARCHAR)
    osi_layer_id INT UNSIGNED,  -- Référence vers la table OSILayer
    category_description TEXT,  -- Description de la catégorie
    category_name VARCHAR(100) NOT NULL,  -- Nom de la catégorie
    FOREIGN KEY (osi_layer_id) REFERENCES OSILayer(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS DeviceSubDevice (
    parent_device_id INT UNSIGNED,  -- Le périphérique parent
    sub_device_id INT UNSIGNED,     -- Le sous-périphérique
    PRIMARY KEY (parent_device_id, sub_device_id),  -- Clé primaire combinée
    FOREIGN KEY (parent_device_id) REFERENCES DeviceType(id) ON DELETE CASCADE,  -- Relation vers DeviceType
    FOREIGN KEY (sub_device_id) REFERENCES DeviceType(id) ON DELETE CASCADE      -- Relation vers DeviceType
) ENGINE=InnoDB DEFAULT CHARSET=utf8;