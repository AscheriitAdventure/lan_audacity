import json
import os
import time
import shutil
from network import Network


class LanAudacity:
    def __init__(
        self,
        software_name: str,
        version_software: str,
        project_name: str,
        save_path: str,
        author: str = None,
    ):
        self.software = software_name
        self.version = version_software
        self.save_path = save_path
        self.char_table = "utf-8"
        self.project_name = project_name
        self.date_unix: float = time.time()
        self.last_update_unix: float = time.time()
        self.author = author
        self.abs_paths = {
            "conf": {"path": "conf", "folders": [], "files": []},
            "db": {
                "path": "db",
                "folders": ["interfaces", "desktop"],
                "files": [],
            },
            "logs": {"path": "logs", "folders": [], "files": ["lan_audacity.log"]},
            "pixmap": {"path": "pixmap", "folders": [], "files": []},
        }
        self.networks = None
        self.links = None
        self.devices = None
        self.pixmap = None

    def create_project(self) -> str:
        if not os.path.exists(f"{self.save_path}/{self.project_name}"):
            os.mkdir(f"{self.save_path}/{self.project_name}")
            with open(
                f"{self.save_path}/{self.project_name}/lan_audacity.json", "w"
            ) as f:
                json.dump(self.__dict__, f, indent=4)
            for key, value in self.abs_paths.items():
                os.mkdir(f"{self.save_path}/{self.project_name}/{value['path']}")
                if value["folders"]:
                    for folder in value["folders"]:
                        os.mkdir(
                            f"{self.save_path}/{self.project_name}/{value['path']}/{folder}"
                        )
                if value["files"]:
                    for file in value["files"]:
                        with open(
                            f"{self.save_path}/{self.project_name}/{value['path']}/{file}",
                            "w",
                        ) as f:
                            f.write("")
            return f"{self.project_name} is created"
        else:
            return f"{self.project_name} already exists"

    def delete_project(self) -> str:
        if os.path.exists(f"{self.save_path}/{self.project_name}"):
            try:
                shutil.rmtree(f"{self.save_path}/{self.project_name}")
                return f"{self.project_name} is deleted"
            except OSError as e:
                return f"Error remove {self.project_name} : {e}"
        else:
            return f"{self.project_name} doesn't exist"

    def add_network(self, network: Network) -> str:
        if self.networks is None:
            self.networks = {"path": "interfaces", "obj_ls": []}
        self.networks["obj_ls"].append(
            {
                "uuid": network.uuid,
                "name": network.name,
                "path": network.abs_path,
                "ls_devices": [],
            }
        )
        self.last_update_unix = time.time()
        with open(f"{self.save_path}/{self.project_name}/lan_audacity.json", "w") as f:
            json.dump(self.__dict__, f, indent=4)
        return f"{network.name} is added to {self.project_name}"

    def remove_network(self, network: Network) -> str:
        if self.networks is not None:
            self.networks["obj_ls"].remove(network.uuid)
            self.last_update_unix = time.time()
            with open(
                f"{self.save_path}/{self.project_name}/lan_audacity.json", "w"
            ) as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{network.name} is removed from {self.project_name}"
        else:
            return f"{network.name} doesn't exist in {self.project_name}"

    def open_project(self) -> str:
        if os.path.exists(self.project_name):
            with open(
                f"{self.save_path}/{self.project_name}/lan_audacity.json", "r"
            ) as f:
                datas = json.load(f)
                self.software = datas["software"]
                self.version = datas["version"]
                self.save_path = datas["save_path"]
                self.char_table = datas["char_table"]
                self.project_name = datas["project_name"]
                self.date_unix = datas["date_unix"]
                self.last_update_unix = datas["last_update_unix"]
                self.author = datas["author"]
                self.abs_paths = datas["abs_paths"]
                # Construct all datas
            return f"{self.project_name} does exist"
        else:
            return f"{self.project_name} doesn't exist"

    def save_project(self) -> str:
        if os.path.exists(self.project_name):
            self.last_update_unix = time.time()
            with open(
                f"{self.save_path}/{self.project_name}/lan_audacity.json", "w"
            ) as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{self.project_name} is saved"
        else:
            return f"{self.project_name} doesn't exist"

    def save_as_project(self, new_path: str, new_project_name: str) -> str:
        if os.path.exists(new_path):
            self.save_path = new_path
            os.rename(self.project_name, new_project_name)
            self.project_name = new_project_name
            with open(f"{new_path}/{self.project_name}/lan_audacity.json", "w") as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{self.project_name} is saved as {new_project_name}"
        else:
            return f"{self.project_name} doesn't exist"


if __name__ == "__main__":
    lan_audacity = LanAudacity(
        "Lan Audacity", "0.0.1", "eyrein-industrie_lans", os.getcwd()
    )
    print(lan_audacity.create_project())
    path = f"{lan_audacity.project_name}/{lan_audacity.abs_paths['db']['path']}/{lan_audacity.abs_paths['db']['folders'][0]}"

    lan_interfaces_1 = Network("192.168.90.0", "255.255.255.0", path, "ZAC Bureaux")
    print(lan_audacity.add_network(lan_interfaces_1))
    lan_interfaces_2 = Network("192.168.2.0", "255.255.255.0", path, "ZAC Expéditions")
    print(lan_audacity.add_network(lan_interfaces_2))
    lan_interfaces_3 = Network("192.168.1.0", "255.255.255.0", path, "ZAC Invités")
    print(lan_audacity.add_network(lan_interfaces_3))
    lan_interfaces_4 = Network("192.168.100.0", "255.255.255.0", path, "ZI")
    print(lan_audacity.add_network(lan_interfaces_4))
    lan_interfaces_5 = Network("192.168.110.0", "255.255.255.0", path, "TAZO")
    print(lan_audacity.add_network(lan_interfaces_5))
    lan_interfaces_6 = Network("192.168.70.0", "255.255.255.0", path, "PARIS")
    print(lan_audacity.add_network(lan_interfaces_6))
    lan_interfaces_7 = Network("192.168.253.0", "255.255.255.0", path, "CHALLENGER")
    print(lan_audacity.add_network(lan_interfaces_7))

#     print(lan_audacity.save_project())
#     time.sleep(10)

#     print(lan_audacity.delete_project())
