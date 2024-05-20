from datetime import datetime
import time


class ClockManager:
    def __init__(self):
        self.__create = time.time()
        self.__last_update = time.time()
        self.type_time = "Unix Timestamp Format"

    @property
    def createUptime(self):
        return self.__create

    @property
    def last_update(self):
        return self.__last_update

    @property
    def describe(self):
        return self.type_time

    @last_update.setter
    def last_update(self, unixtime: float):
        self.__last_update = unixtime

    def set_lastUpdate(self):
        self.last_update = time.time()
    def get_lastdt(self):
        return datetime.utcfromtimestamp(self.last_update)
    def get_creadt(self):
        return datetime.utcfromtimestamp(self.createUptime)

    def __str__(self):
        return f"1er Scan: {self.get_creadt()}, last Scan: {self.get_lastdt()}"


if __name__ == '__main__':
    clock = ClockManager()
    print(clock)
    time.sleep(4)
    clock.set_lastUpdate()
    print(clock)
