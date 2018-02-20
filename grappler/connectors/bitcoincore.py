import struct, logging, time
from hashlib import sha256
from .connector import Connector
from .. import version

magic_values = {
    "mainnet": 0xD9B4BEF9,
    "testnet": 0xDAB5BFFA,
    "testnet3": 0x0709110B,
    "namecoin": 0xFEB4BEF9
}

protocol_version = 70015


class BitcoinCoreConnector(Connector):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(type(self).__name__)
        if kwargs["ssl"] is True:
            self.log.log(15, "Note, Bitcoin P2P doesn't use (or need) SSL.  Disabling.")
            kwargs["ssl"] = False
        super(type(self), self).__init__(*args, **kwargs)
        self.user_agent = 'grappler_{}_{}'.format(version.author_short, version.version)
        self._version()

    @staticmethod
    def _add_header(network, command, payload=b''):
        header = struct.pack(
            '<L 12s I',
            magic_values[network],
            command.encode(),
            len(payload)
        )
        checksum = sha256(sha256(payload).digest()).digest()[:4]
        return header + checksum + payload

    def receive(self):
        header = self.connection.recv(24)
        magic_bytes, command, payload_size, checksum = struct.unpack('4s 12s I 4s', header)
        command = command.decode().split('\0', 1)[0]
        payload = self.connection.recv(payload_size)
        self.log.log(4, "_receive {}".format(command))
        assert magic_bytes == struct.pack('<L', magic_values[self.network])
        assert checksum == sha256(sha256(payload).digest()).digest()[:4]
        return command, payload

    def send(self, command, payload=b''):
        self.log.log(5, "send {}".format(command))
        data = self._add_header(self.network, command, payload)
        self.connection.send(data)
        return self.receive()

    def _version(self):
        version = struct.pack('<L', protocol_version)
        services = struct.pack('<Q', 0)
        timestamp = struct.pack('<q', int(time.time()))
        addr_recv_services = struct.pack('<Q', 0)
        addr_recv_ip = struct.pack('>16s', b'')
        addr_recv_port = struct.pack('>H', self.port)
        addr_trans_services = struct.pack('<Q', 0)
        addr_trans_ip = struct.pack('>16s', b'')
        addr_trans_port = struct.pack('>H', self.connection.getsockname()[1])
        nonce = struct.pack('<Q', 0)
        user_agent = self.user_agent.encode()
        user_agent_bytes = struct.pack('<B', len(user_agent))
        start_height = struct.pack('<I', 0)
        relay = struct.pack('<B', 0)
        data = version + \
            services + \
            timestamp + \
            addr_recv_services + \
            addr_recv_ip + \
            addr_recv_port + \
            addr_trans_services + \
            addr_trans_ip + \
            addr_trans_port + \
            nonce + \
            user_agent_bytes + \
            user_agent + \
            start_height + \
            relay
        self.send("version", data)
        if self.receive() == ('verack', b''):
            self.send("verack")
            self.receive() # superfluous sendheaders message
            self.receive()
            self.receive()
