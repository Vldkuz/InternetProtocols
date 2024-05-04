from scapy.all import *

DEFAULT_PORT = 33434
DEFAULT_MAX_HOPS = 30
DEFAULT_TIMEOUT = 1
END_TYPE = 3
START_TTL = 1


class Trace:
    def __init__(self, dst: str, max_hops: int = DEFAULT_MAX_HOPS, timeout: int = DEFAULT_TIMEOUT):
        self.__dst = socket.gethostbyname(dst)  # Храним только IP-адреса
        self.__max_hops = max_hops
        self.__timeout = timeout
        self.__port = DEFAULT_PORT
        self.__ip_list = []

    def trace(self) -> list:
        ttl = START_TTL
        while True:
            pack = IP(dst=self.__dst, ttl=ttl) / UDP(dport=self.__port)
            reply = sr1(pack, timeout=self.__timeout, verbose=False)

            if reply is not None:
                self.__ip_list.append(reply.src)
                if reply.type == END_TYPE:
                    break

            if ttl > self.__max_hops:
                break

            ttl += 1

        self.__ip_list.append(self.__dst)
        return self.__ip_list

    def get_ip_list(self) -> list:
        return self.__ip_list
