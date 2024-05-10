import binascii
import logging
import os
import socket
import sys

from dotenv import load_dotenv
from cache import Cache
from dns_packets.config_dns import DNSConfig
from dns_packets.dns_packet_creator import DNSCreator
from dns_packets.dns_packet_parser import DNSParser
from typeclasses.creator_typeclasses.record_answer import Answer
from utils.utils_dns_config import to_creator
from utils.utils_server import resolve_name

LOG_LEVEL_MAPPER = {'INFO': logging.INFO, 'DEBUG': logging.DEBUG, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR,
                    'CRITICAL': logging.CRITICAL}

load_dotenv()

# Здесь можем сконфигурировать сервер с помощью переменных окружения:
# PORT - отвечает за порт работы сервера
# LOG_LEVEL - отвечает за уровень логирования
# CACHE_FILE - отвечает за имя файла для сериализации и десериализации кеша
# IP_SERVER - отвечает за IP интерфейса, на котором будет поднят сервер
# ROOT_DNS - отвечает за IP forward сервера, для разрешения днс запросов

PORT = int(os.getenv('PORT')) or 53
LOG_LEVEL = os.getenv('LOG_LEVEL') or logging.INFO
CACHE_FILE_SERIALIZE = os.getenv('CACHE_FILE') or 'cache.json'
IP_SERVER = os.getenv('IP_SERVER') or '127.0.0.1'
ROOT_DNS = os.getenv('ROOT_DNS') or '8.8.8.8'

logging.basicConfig(level=LOG_LEVEL, filename='server.log', filemode='a')
logging.info(f"Starting logging. PORT: {PORT}, LOG_LEVEL: {LOG_LEVEL}")


def main_loop(server_socket: socket, root_dns: str, hot_cache: Cache):
    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            logging.info(f'{addr} connected')

            hex_data = binascii.b2a_hex(data)
            logging.info(f'read from {addr} : {hex_data}')
            query_packet: DNSParser = DNSParser(hex_data)
            std_dns_config = DNSConfig().from_parsed_packet(query_packet)
            std_dns_config.QR = 1

            for query in query_packet.queries_list:
                answer = hot_cache.get(query.qname, query.type_record)

                if answer is None:
                    answer_query = resolve_name(query.qname, query.type_record, query.class_record, root_dns)
                    logging.info(f'{query.qname} : {query.type_record} was resolved from forwarder')

                    for resolved_answer in answer_query.answers_list:
                        rdata = to_creator(resolved_answer)
                        hot_cache.push(resolved_answer.name, resolved_answer.type_record, rdata, resolved_answer.ttl)
                        std_dns_config.ANSWERS.append(
                            Answer(resolved_answer.name, resolved_answer.type_record, resolved_answer.class_record,
                                   resolved_answer.ttl, rdata))
                else:
                    logging.info(f'{query.qname}|{query.type_record} was get from cache')
                    std_dns_config.ANSWERS.append(
                        Answer(query.qname, query.type_record, query.class_record, answer[1], answer[0]))

            answer_dns = DNSCreator(std_dns_config).to_bin()

            if len(answer_dns) % 2:
                answer_dns = '0' + answer_dns

            server_socket.sendto(bytes.fromhex(answer_dns), addr)

        except KeyboardInterrupt:
            logging.info('Ctrl+C received, shutting down')
            hot_cache.to_json(CACHE_FILE_SERIALIZE)
            sys.exit(0)
        except OSError:
            logging.error("Network is unreachable")
        except Exception as err:
            logging.error(err)
            continue


if __name__ == '__main__':
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
            cache: Cache = Cache()
            cache.from_json(CACHE_FILE_SERIALIZE)
            server.bind((IP_SERVER, PORT))
            logging.info('Server is running, press ctrl+c to stop')
            main_loop(server, ROOT_DNS, cache)
    except Exception as error:
        logging.error(error)
