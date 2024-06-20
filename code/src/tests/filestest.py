import time
import json
import os

class ClockManager:
    def __init__(
            self, 
            time_start: float = time.time(),
            time_list: list[float] = []
        ) -> None:
        self.__clock_created: float = time_start
        self.__clock_list: list[float] = time_list
        if not time_list:
            self.__clock_list.append(self.clockCreated)
        self.type_time = "Unix Timestamp Format"

    @property
    def clockCreated(self) -> float:
        return self.__clock_created
    
    @clockCreated.setter
    def clockCreated(self, value: float) -> None:
        self.__clock_created = value

    @property
    def clockList(self) -> list[float]:
        return self.__clock_list
    
    @clockList.setter
    def clockList(self, value: list[float]) -> None:
        self.__clock_list = value

    def add_clock(self) -> None:
        self.clockList.append(time.time())
    
    def get_clock_last(self) -> float:
        return self.clockList[-1]

    def get_clock_diff(self) -> float:
        return self.clockList[-1] - self.clockList[-2]
    
    def dict_return(self) -> dict:
        return {
            "clock_created": self.__clock_created,
            "clock_list": self.__clock_list,
            "type_time": self.type_time
        }

    @staticmethod
    def conv_unix_to_datetime(unix_time: float) -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(unix_time))

    def __str__(self) -> str:
        return f"ClockManager: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.clockCreated))}"

# Step 1: Create a ClockManager object
clock_manager = ClockManager()

# Step 2: Open the json file
json_file_path = os.getcwd() + "/clock_manager.json"
try:
    with open(json_file_path, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}

# Step 3: Read the json file
if data:
    print("Content of the JSON file:")
    print(data)
else:
    print("The json file is empty")

# Step 4: Dump the json file
if data:
    clock_manager.clockCreated = data.get('clock_created', clock_manager.clockCreated)
    clock_manager.clockList = data.get('clock_list', clock_manager.clockList)
    clock_manager.add_clock()
    print("The json file content has been loaded into the ClockManager object")
with open(json_file_path, 'w') as f:
    json.dump(clock_manager.dict_return(), f)
# Step 5: Print the content of the ClockManager object
print(clock_manager)
