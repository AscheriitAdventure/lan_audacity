import subprocess


class NetDevice:
    def __init__(self, ip: str):
        self._ip = ip
        self.ping = False
        self.info = None

    def get_ip(self):
        return self._ip

    def get_ping(self):
        return self.ping

    def set_ping(self):
        try:
            subprocess.run(["ping", "-c", "4", self._ip], check=True)
            self.ping = True
        except subprocess.CalledProcessError:
            self.ping = False
