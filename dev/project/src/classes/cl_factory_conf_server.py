from enum import Enum
from typing import Union, Any


from sql_server import MySQLConnection as SQLServer

class FactoryConfData:
    class RWX(Enum):
        READ = "r"
        WRITE = "w"
        APPEND = "a"
            
    def __init__(self, server: Union[SQLServer, Any]): # Any à changer quand j'aurai fait les autres classes
        self.server = server