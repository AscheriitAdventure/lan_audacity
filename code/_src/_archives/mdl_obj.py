import qtawesome as qta
import time


class ClockManager:
    def __init__(self):
        self.__clock_created: float = time.time()
        self.__clock_list: list[float] = []
        self.__clock_list.append(self.clock_created)
        self.type_time = "Unix Timestamp Format"

    @property
    def clock_created(self):
        return self.__clock_created

    @property
    def clock_list(self):
        return self.__clock_list

    def add_clock(self):
        self.clock_list.append(time.time())

    def get_clock_list(self):
        return self.clock_list

    def get_clock_created(self):
        return self.clock_created

    def get_clock_last(self):
        return self.clock_list[-1]

    def get_clock_diff(self):
        return self.clock_list[-1] - self.clock_list[-2]

    @staticmethod
    def conv_unix_to_datetime(unix_time: float):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(unix_time))

    def __str__(self) -> str:
        return f"ClockManager: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.clock_created))}"


class IconObj:
    def __init__(
            self,
            icon: any = qta.icon('fa5r.question-circle'),
            flag: str = 'Objet Non-Identifié'):
        self.__pix_icon = icon
        self.__pix_flag = flag

    @property
    def pix_icon(self):
        return self.__pix_icon

    @pix_icon.setter
    def pix_icon(self, value: any):
        self.__pix_icon = value

    @property
    def flag_icon(self):
        return self.__pix_flag

    @flag_icon.setter
    def flag_icon(self, value: str):
        if value != '' or value is not None:
            self.__pix_flag = value


class Device:
    def __init__(
            self,
            name: str = "Unknown",
            ip: str = "0.0.0.0",
            mac: str = "00:00:00:00:00:00",
            mask: str = "255.0.0.0",
    ):
        self.__name: str = name
        self.__ip: str = ip
        self.__mac: str = mac
        self.__mask: str = mask
        self.__clock_manager: ClockManager = ClockManager()
        self.__icon_obj: IconObj | None = None


    @property
    def clock_time(self):
        return self.__clock_manager
    @property
    def icon_obj(self):
        return self.__icon_obj

    @icon_obj.setter
    def icon_obj(self, value: any):
        if value is not None:
            self.__icon_obj = value

    def set_default_icon(self) -> IconObj:
        computer_unknown: any = qta.icon('fa5s.desktop', 'fa5s.question',
                                         options=[{'scale_factor': 0.5}, {'color': 'blue'}])
        text_flag = f"{self.name}({self.ipv4})"
        icon_obj = IconObj(computer_unknown, text_flag)
        return icon_obj

    @property
    def name(self):
        return self.__name

    @property
    def ipv4(self):
        return self.__ip

    @property
    def mac(self):
        return self.__mac

    @property
    def mask(self):
        return self.__mask

    @name.setter
    def name(self, name: str):
        if name != "" or name is not None:
            self.__name = name

    @ipv4.setter
    def ipv4(self, ip: str):
        if self.true_ip(ip):
            self.__ip = ip
        else:
            raise ValueError("IP address is not valid")

    @mac.setter
    def mac(self, mac: str):
        if self.true_mac(mac):
            self.__mac = mac
        else:
            raise ValueError("MAC address is not valid")

    @mask.setter
    def mask(self, mask: str):
        if self.true_ip(mask):
            self.__mask = mask
        else:
            raise ValueError("Mask address is not valid")

    def __str__(self) -> str:
        return f"NetDevice: {self.name}/{self.ipv4}/{self.mac}"

    def set_mask(self):
        self.clock_time.add_clock()
        try:
            interfaces = netifaces.interfaces()
            for interface in interfaces:
                addr = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addr:
                    for addr_info in addr[netifaces.AF_INET]:
                        if 'addr' in addr_info and addr_info['addr'] == self.ipv4:
                            self.mask = addr_info['netmask']
        except Exception as e:
            logging.warning("Une erreur s'est produite lors de la récupération du masque de sous-réseau:", e)

    def set_name(self):
        self.clock_time.add_clock()
        try:
            self.name = socket.gethostbyaddr(self.ipv4)[0]
        except socket.herror as e:
            logging.warning(f"Erreur lors de la resolution DNS pour l'adresse IP {self.ipv4}: {e}")

    def set_addr_mac(self):
        self.clock_time.add_clock()
        try:
            arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=self.ipv4)
            result = srp(arp_request, timeout=3, verbose=False)[0]
            for _, received in result:
                self.__mac = received.hwsrc
                break
        except Exception as e:
            logging.warning(f"Erreur lors de la récupération de l'adresse MAC pour l'adresse IP {self.ipv4}: {e}")

    @staticmethod
    def true_ip(ipv4: str) -> bool:
        ipv4_pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
        match = re.match(ipv4_pattern, ipv4)
        if match:
            if all(0 <= int(octet) <= 255 for octet in match.groups()):
                return True
        return False

    @staticmethod
    def true_mac(mac: str) -> bool:
        mac_pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
        match = re.match(mac_pattern, mac)
        if match:
            return True
        return False
