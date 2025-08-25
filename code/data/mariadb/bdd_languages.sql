CREATE DATABASE IF NOT EXISTS lan_audacity_sql_server 
DEFAULT CHARACTER SET utf8 
COLLATE utf8_general_ci;

USE lan_audacity_sql_server;

CREATE TABLE IF NOT EXISTS languages (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    language_name VARCHAR(255) NOT NULL,
    language_code VARCHAR(255) NOT NULL,
    language_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS lan_audacity (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    lan_audacity_name VARCHAR(255) NOT NULL,
    start_version VARCHAR(255) NOT NULL,
    last_version VARCHAR(255) NOT NULL,
    lan_audacity_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS lan_audacity_network (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    lan_audacity_id INT UNSIGNED NOT NULL,
    network_id INT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lan_audacity_id) REFERENCES lan_audacity(id),
    FOREIGN KEY (network_id) REFERENCES network(network_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS authors (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    authors_id INT UNSIGNED NOT NULL,
    project_id INT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (authors_id) REFERENCES users(id),
    FOREIGN KEY (project_id) REFERENCES lan_audacity(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;