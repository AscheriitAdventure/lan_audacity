CREATE DATABASE IF NOT EXISTS db_lanAudacity
DEFAULT CHARACTER SET utf8 
COLLATE utf8mb4_general_ci;

USE db_lanAudacity;

/* Table structure for table `ClockManager` */
CREATE TABLE IF NOT EXISTS ClockManager (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    created_at FLOAT NOT NULL,
    updated_at FLOAT NOT NULL,
    type_time VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS UpdateAtList (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    clock_manager_id INT UNSIGNED,
    update_at FLOAT NOT NULL,
    FOREIGN KEY (clock_manager_id) REFERENCES ClockManager(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table structure for table `Users` */
CREATE TABLE IF NOT EXISTS Users (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    users_name VARCHAR(255) NOT NULL,
    users_password VARCHAR(255) NOT NULL,
    users_email VARCHAR(255),
    users_is_active BOOLEAN DEFAULT 1,
    clock_manager_id INT UNSIGNED,
    FOREIGN KEY (clock_manager_id) REFERENCES ClockManager(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS Roles (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    roles_name VARCHAR(255) NOT NULL,
    roles_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO roles (roles_name, roles_description) VALUES 
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

CREATE TABLE IF NOT EXISTS LanAudacity (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    lan_audacity_name VARCHAR(255) NOT NULL,
    start_version VARCHAR(255) NOT NULL,
    last_version VARCHAR(255) NOT NULL,
    lan_audacity_description TEXT,
    clock_manager_id INT UNSIGNED,
    FOREIGN KEY (clock_manager_id) REFERENCES ClockManager(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
