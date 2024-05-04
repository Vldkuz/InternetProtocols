import logging
import os
import socket
import binascii
from socket import SocketKind
from dotenv import load_dotenv
from cache import Cache
from dns_packets.dns_packet_parser import DNSPacketParser

TRANSPORT_PROTO_MAPPER = {'UDP': socket.SOCK_DGRAM, 'TCP': socket.SOCK_STREAM}
LOG_LEVEL_MAPPER = {'INFO': logging.INFO, 'DEBUG': logging.DEBUG, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR,
                    'CRITICAL': logging.CRITICAL}
load_dotenv()

PORT = os.getenv('PORT') or 53
TRANSPORT: SocketKind | None = TRANSPORT_PROTO_MAPPER.get(os.getenv('TRANSPORT_PROTO')) or socket.SOCK_DGRAM
LOG_LEVEL = os.getenv('LOG_LEVEL') or logging.INFO
CACHE_FILE_SERIALIZE = os.getenv('CACHE_FILE') or 'cache.json'

logging.basicConfig(level=LOG_LEVEL, filename='server.log', filemode='a')

logging.info(
    f"Server starting logging. Initial parameters PORT: {PORT}, TRANSPORT_PROTOCOL: {TRANSPORT}, LOG_LEVEL: {LOG_LEVEL}")


def load_from_socket(conn) -> bytes:
    data = b''

    while True:
        new = connection.recv(1024)
        data += new

        if new is None:
            break

    return data


def resolve_name_or_ip(name: str):
    pass


try:
    socket = socket.socket(socket.AF_INET, TRANSPORT)
    socket.bind(('', PORT))
    socket.listen(10)
    logging.info('Server is running, press ctrl+c to stop')
    cache: Cache = Cache().from_json(CACHE_FILE_SERIALIZE)

    while True:
        connection, addr = socket.accept()
        logging.info(f'{addr} connected')

        loaded_data = load_from_socket(connection)
        hex_data = binascii.b2a_hex(loaded_data)
        logging.info(f'read from {addr} : {hex_data}')

        parsed_packet: DNSPacketParser = DNSPacketParser(hex_data)

        for query in parsed_packet.queries_list:
            record = query.type_record
            name_or_ip = query.qname
            record_cached = cache.get(name_or_ip, record)





except Exception as e:
    logging.error(e)
