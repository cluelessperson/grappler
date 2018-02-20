import logging, socket, ssl


class Connector:
    def __init__(self, host, port, ssl=False, timeout=5, network='mainnet'):
        self.log.log(15, "Starting...")
        self.host = host
        self.port = port
        self.ssl = ssl
        self.timeout = timeout
        self.network = network

        self.connection = None
        self._connect()

    def _connect(self):
        self.log.log(10, "_connect {} {}".format(self.host, self.port))
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.settimeout(self.timeout)
        if self.ssl:
            self.connection = ssl.wrap_socket(self.connection)
        self.connection.connect((self.host, self.port))
