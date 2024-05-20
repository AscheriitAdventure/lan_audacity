class IdSSH:
    def __init__(self, _ip: str, _username: str, _pwd: str):
        self.ip = _ip
        self.username = _username
        self.password = _pwd

    @property
    def username(self):
        return self.__username
    @property
    def password(self):
        return self.__password
    @username.setter
    def username(self, username: str):
        if username is not '':
            self.__username = username
        else:
            raise ValueError('Invalid username')

    @password.setter
    def password(self, password: str):
        if password is not '':
            self.__password = password
        else:
            raise ValueError('Invalid password')

    def __str__(self):
        return f"ssh {self.username}@{self.ip} // {self.password}"

    def save(self, device_port: int = 22):
        message = f"ssh {self.username}@{self.ip} -p {device_port}\n"
        with open('ssh_keygens.txt', 'a') as f:
            f.write(message)
