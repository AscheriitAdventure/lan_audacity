CREATE DATABASE IF NOT EXISTS lan_audacity_sql_server 
DEFAULT CHARACTER SET utf8 
COLLATE utf8_general_ci;

USE lan_audacity_sql_server;

CREATE TABLE IF NOT EXISTS users (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY
    users_name VARCHAR(255) NOT NULL,
    users_password VARCHAR(255) NOT NULL,
    users_email VARCHAR(255),
    users_is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO users (username, password, email) 
VALUES 
("root", "Root846*", "root@localhost"),
("admin", "Admin813+", "admin@localhost"),
("user", "User792-", "user@localhost");

CREATE TABLE IF NOT EXISTS roles (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY
    name VARCHAR(255) NOT NULL,
    roles_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO roles (name, description) VALUES 
("ROLE_ROOT", "Rôle qui a tous les droits, a désactiver dès que possible"),
("ROLE_ADMIN", "Rôle qui à tous les droits sur la base de données, mais aucunes sur l'application"),
("ROLE_USER", "Rôle de base pour les utilisateurs de l'application"),
("ROLE_GUEST", "Rôle pour les utilisateurs non connectés");

CREATE TABLE IF NOT EXISTS user_roles (
    user_id INT UNSIGNED,
    role_id INT UNSIGNED,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES roles(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO user_roles (user_id, role_id) VALUES 
(1, 1),
(2, 2),
(3, 3);

CREATE TABLE IF NOT EXISTS user_logs (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY
    user_id INT UNSIGNED,
    user_log_object TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



