import nmap
import logging


class NmapForm:
    def __init__(self, target: str):
        self.__target = target
        self.__ports: list[NmapPort] = []
        self.__os: list[NmapOs] = []

    @property
    def portsList(self):
        return self.__ports

    @property
    def osList(self):
        return self.__os

    def scanPort(self):
        host = self.__target
        nm = nmap.PortScanner()
        nm.scan(hosts=host, arguments="-sV -p 1-65535 -v")
        logging.info(nm.command_line())
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                l_port = nm[host][proto].keys()
                for port in l_port:
                    state = nm[host][proto][port]["state"]
                    service = nm[host][proto][port]["name"]
                    version = nm[host][proto][port]["version"]
                    new_port = NmapPort(port, state, service, version)
                    self.__ports.append(new_port)

    def scanOs(self):
        host = self.__target
        nm = nmap.PortScanner()
        nm.scan(hosts=host, arguments="-O -A -v")
        logging.info(nm.command_line())
        for host in nm.all_hosts():
            for osmatch in nm[host]["osmatch"]:
                os_name = osmatch["name"]
                os_accuracy = osmatch["accuracy"]
                os_type = osmatch["osclass"]["type"]
                os_vendor = osmatch["osclass"]["vendor"]
                os_family = osmatch["osclass"]["osfamily"]
                new_os = NmapOs(os_name, os_accuracy, os_type, os_vendor, os_family)
                self.__os.append(new_os)

    def ports_remove(self, port: int):
        for i in self.__ports:
            if i.port == port:
                self.__ports.remove(i)
                break

    def os_remove(self, os_name: str):
        for i in self.__os:
            if i.osName == os_name:
                self.__os.remove(i)
                break

    def ports_clear(self):
        self.__ports.clear()

    def os_clear(self):
        self.__os.clear()

    def ports_add(self, port: int, state: str, service: str, version: str):
        new_port = NmapPort(port, state, service, version)
        self.__ports.append(new_port)


class NmapPort:
    def __init__(self, port: int, state: str, service: str, version: str):
        self.__port = port
        self.__state = state
        self.__service = service
        self.__version = version

    @property
    def port(self):
        return self.__port

    @property
    def state(self):
        return self.__state

    @property
    def service(self):
        return self.__service

    @property
    def version(self):
        return self.__version


class NmapOs:
    def __init__(
        self,
        os_name: str,
        os_accuracy: int,
        os_type: str,
        os_vendor: str,
        os_family: str,
    ) -> None:
        self.__os_name = os_name
        self.__os_accuracy = os_accuracy
        self.__os_type = os_type
        self.__os_vendor = os_vendor
        self.__os_family = os_family

    @property
    def osName(self):
        return self.__os_name

    @property
    def osAccuracy(self):
        return self.__os_accuracy

    @property
    def osType(self):
        return self.__os_type

    @property
    def osVendor(self):
        return self.__os_vendor

    @property
    def osFamily(self):
        return self.__os_family
