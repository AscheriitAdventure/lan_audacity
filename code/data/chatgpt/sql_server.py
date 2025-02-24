import logging
from mysql.connector import Error
import mysql.connector

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MySQLConnection:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                logging.info("Connection to MySQL database was successful")
        except Error as e:
            logging.error(f"Error while connecting to MySQL: {e}")

    def disconnect(self):
        if self.connection.is_connected():
            self.connection.close()
            logging.info("MySQL connection is closed")

    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            logging.info("Query executed successfully")
        except Error as e:
            logging.error(f"Error: '{e}'")
        finally:
            cursor.close()

    def fetch_data(self, query):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            logging.info("Data fetched successfully")
            return result
        except Error as e:
            logging.error(f"Error: '{e}'")
        finally:
            cursor.close()