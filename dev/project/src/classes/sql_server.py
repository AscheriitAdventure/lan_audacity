import logging
from mysql.connector import Error
import mysql.connector
from typing import Any
import inspect

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MySQLConnection:
    def __init__(self, host, database, user, password) -> None:
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self) -> None:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                charset="utf8mb4", # passé mysql_8 mettre utf8mb3
                collation="utf8mb4_general_ci", # passé mysql_8 mettre utf8mb3_general_ci
            )
            if self.connection.is_connected():
                logging.info(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Connection to MySQL database was successful")
        except Error as e:
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error while connecting to MySQL: {e}")

    def disconnect(self) -> None:
        if self.connection.is_connected():
            self.connection.close()
            logging.info(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: MySQL connection is closed")

    def execute_query(self, query) -> None:
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Query executed successfully")
        except Error as e:
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error: '{e}'")
        finally:
            cursor.close()
    
    def execute_query_id(self, query) -> int:
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            self.connection.commit()
            result = cursor.lastrowid
            logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Query executed successfully")
            return result
        except Error as e:
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error: '{e}'")
        finally:
            cursor.close()

    def fetch_data(self, query) -> Any:
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Data fetched successfully")
            return result
        except Error as e:
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error: '{e}'")
        finally:
            cursor.close()