from src.core.sql_server import MySQLConnection as SQLServer
from typing import Any
import logging


def findQuery(name: str, data: Any) -> dict | None:
    for query in data:
        if query["name"] == name:
            logging.debug(f"Query found: {name}")
            return query
    return None


def queryForm(command: str, values: tuple | list) -> str:
    placeholders = ", ".join(
        f"'{value}'" if not isinstance(value, (int, float)) else str(value)
        for value in values
    )
    logging.debug(f"Query form: {command}({placeholders});")
    return f"{command}({placeholders});"

import time

database = SQLServer(
    host="localhost",
    database="db_test",
    user="root",
    password="root"
)

database.connect()

# Query
list_query = [
    {
        "name": "showTables",
        "sql": "SHOW TABLES"
    },
    {
        "name": "getAllClock",
        "sql": "SELECT * FROM clockmanager"
    }
]

for query in list_query:
    result = database.fetch_data(query["sql"])
    print(result)

actions_query = [
    {
        "name": "createClock",
        "sql": "INSERT INTO clockmanager (created_at, updated_at, type_time) VALUES ",
        "test_var": [time.time(), time.time(), "Unix Timestamp Format"]
    },
    {
        "name": "updateClock",
        "sql": [
            "INSERT INTO updateatlist (clock_manager_id, updated_at) VALUES ",
            "UPDATE clockmanager SET updated_at = ? WHERE id = ?",
        ],
        "test_var": [1, time.time()]
    },
]

for action in actions_query:
    if isinstance(action["sql"], list):
        # Cas spécial : plusieurs commandes
        for idx, sql in enumerate(action["sql"]):
            query = queryForm(sql, action["test_var"] if idx == 0 else action["test_var"][1:])
            print(query)
            database.execute_query(query)
    else:
        # Une seule commande
        query = queryForm(action["sql"], action["test_var"])
        print(query)
        database.execute_query(query)

result = database.fetch_data(findQuery("getAllClock", list_query)["sql"])
if result:
    print(result)
# si le nom de la requête est trouvé
# alors, nous exécutons la requête

database.disconnect()
