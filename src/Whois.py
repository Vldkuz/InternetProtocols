import socket

DEFAULT_RIR_LIST = ['ripe', 'arin', 'apnic', 'afrinic', 'lacnic']
DEFAULT_PORT = 43


class Whois:
    def __init__(self):
        self.__info_ip = {}

    def get_info(self, ip: str) -> dict[str, str]:
        for rir in DEFAULT_RIR_LIST:
            res = str()
            prep_rir = f'whois.{rir}.net'
            sock = socket.create_connection((prep_rir, DEFAULT_PORT))
            sock.sendall(f'{ip}\n'.encode('utf-8'))

            while True:
                buf = sock.recv(1024).decode('utf-8')
                res += buf
                if len(buf) == 0:
                    break
            result = self.parse_by_rir(rir, res)

            if result is not None:
                return result
        return {"Description": "", "Country": "", "AS": ""}

    def get_info_list_ip(self, list_ip: list[str]) -> dict[str, str]:
        for ip in list_ip:
            self.__info_ip[ip] = self.get_info(ip)
        return self.__info_ip

    def get_info_list(self):
        return self.__info_ip

    @staticmethod
    def parse_by_rir(rir: str, res: str) -> dict[str, str]:
        info = {}
        for line in res.splitlines():
            if rir == 'ripe' or rir == 'apnic' or rir == 'afrinic':
                if line.startswith('descr:') and len(line[len('descr:'):].strip()) > 0:
                    info['Description'] = line[len('descr:'):].strip()
                if line.startswith('country:') and len(line[len('country'):].strip()) > 0:
                    info['Country'] = line[len('country:'):].strip()
                if line.startswith('origin:') and len(line[len('origin:'):].strip()) > 0:
                    info['AS'] = line[len('origin:'):].strip()
            if rir == 'arin':
                if line.startswith('OrgName:') and len(line[len('OrgName:'):].strip()) > 0:
                    info["Description"] = line[len('OrgName:'):].strip()
                if line.startswith('Country:') and len(line[len('Country:'):].strip()) > 0:
                    info["Country"] = line[len('Country:'):].strip()
                if line.startswith('OriginAS:') and len(line[len('OriginAS:'):].strip()) > 0:
                    info["AS"] = line[len('OriginAS:'):].strip()
            if rir == 'lacnic':
                if line.startswith('aut-num:') and len(line[len('aut-num'):].strip()) > 0:
                    info["AS"] = line[len('aut-num:'):].strip()
                if line.startswith('country:') and len(line[len('country:'):].strip()) > 0:
                    info['Country'] = line[len('country:'):].strip()
                if line.startswith('owner:') and len(line[len('owner:'):].strip()) > 0:
                    info['Description'] = line[len('owner:'):].strip()

        if len(info) == 3:
            return info
