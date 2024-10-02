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

