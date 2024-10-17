from dataclasses import dataclass, field
import mysql.connector
import os
import logging
import time
import uuid
from typing import Optional

from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

from src.components.functionsExt import ip_to_cidr, cidr_to_ip


@dataclass
class OsSys:
    name: str
    version: str

    def exec_os(self) -> bool:
        if self.name in ["Windows", "Linux", "Darwin"]:
            return True
        else:
            logging.error(
                f"Operating System '{self.name} {self.version}' not supported."
            )
            return False

    def exec_software(self, softwares: Optional[list]) -> int:
        # search for nmap, docker, and python
        if softwares is not None:
            software_list = softwares
        else:
            software_list = ["docker", "docker-compose", "nmap", "python"]
        var_i = 0
        if self.name == "Windows":
            for software in software_list:
                if os.system(f"where {software} >nul 2>nul") == 0:
                    logging.info(f"{software} is installed.")
                else:
                    logging.warning(f"{software} is not installed.")
                    var_i += 1
        elif self.name in ["Linux", "Darwin"]:
            for software in software_list:
                if os.system(f"which {software} > /dev/null 2>&1") == 0:
                    logging.info(f"{software} is installed.")
                else:
                    logging.warning(f"{software} is not installed.")
                    var_i += 1
        else:
            logging.error(f"Operating System '{self.name}' not supported.")
            var_i += 1

        return var_i


@dataclass
class MariaDB_Docker:
    root_password: str
    database: str
    user: str
    password: str
    port: int

    def connect(self) -> PooledMySQLConnection | MySQLConnectionAbstract:
        """
        Connexion à la base de données MariaDB
        """
        return mysql.connector.connect(
            host="localhost",
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )

    def insert_request(self, table: str, data: dict) -> None:
        """
        table : str - Nom de la table
        data : dict - Dictionnaire des valeurs à insérer (les clés sont les noms des colonnes)
        """
        placeholders = ", ".join(["%s"] * len(data))
        columns = ", ".join(data.keys())
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        logging.debug(sql)
        logging.debug(data)
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(sql, list(data.values()))
            conn.commit()
        except mysql.connector.Error as e:
            logging.error(e)
        finally:
            cursor.close()
            conn.close()

    def fetch_request(
        self, table: str, columns: str | list = "*", condition: Optional[str] = None
    ) -> list:
        """
        table : str - Nom de la table
        columns : str ou list - Colonnes à sélectionner (par défaut '*')
        condition : str - Condition pour filtrer les données (facultatif)
        """
        sql = f"SELECT {', '.join(columns) if isinstance(columns, list) else columns} FROM {table}"
        if condition:
            sql += f" WHERE {condition}"
        logging.debug(sql)
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
        except mysql.connector.Error as e:
            logging.error(e)
        finally:
            cursor.close()
            conn.close()

        return result


@dataclass
class MongoDB_Docker:
    user: str
    password: str
    port: int


@dataclass
class User:
    username: str = field(default_factory=os.getlogin())
    password: str = field(default_factory="")


@dataclass
class UserHistory:
    user: User = field(default_factory=User)
    history: list = field(default_factory=[])

    def addFolderPath(self, folder_path: str) -> None:
        # S'il existe dans l'historique
        if folder_path in self.history:
            self.history.remove(folder_path)
            self.history.append(folder_path)
        else:
            self.history.append(folder_path)

    def removeFolderPath(self, folder_path: str) -> None:
        self.history.remove(folder_path)

    def clearHistory(self) -> None:
        self.history.clear()

    def last10Folders(self) -> list:
        return self.history[-10:]


@dataclass
class WebAddress:
    ipv4: Optional[str] = None
    mask_ipv4: Optional[str] = None
    ipv4_public: Optional[str] = None
    cidr: Optional[str] = None
    ipv6_local: Optional[str] = None
    ipv6_global: Optional[str] = None
    domain_name: Optional[str] = None

    def addressIPv4_values(self) -> None:
        if self.ipv4 and self.mask_ipv4:
            self.cidr = ip_to_cidr(self.ipv4, self.mask_ipv4)
        else:
            self.cidr = None

        if self.cidr:
            self.ipv4, self.mask_ipv4 = cidr_to_ip(self.cidr)
        else:
            self.ipv4 = None
            self.mask_ipv4 = None


@dataclass
class ClockManager:
    clock_created: float = field(default_factory=time.time())
    clock_list: Optional[list[float]] = field(default_factory=[])
    type_time: str = field(default_factory="Unix Timestamp Format")

    def addClock(self) -> None:
        self.clock_list.append(time.time())

    def clearClock(self) -> None:
        self.clock_list.clear()

    def lastClock(self) -> float:
        if not self.clock_list:
            return self.clock_created
        else:
            return self.clock_list[-1]


@dataclass
class Net_Object:
    uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = field(default_factory="Object Name Undefined")
    web_address: WebAddress = field(default_factory=WebAddress)
    clock_manager: ClockManager = field(default_factory=ClockManager)
