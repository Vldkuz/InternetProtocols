import unittest

from config_dns import DNSConfig
from dns_packet_parser import DNSPacketParser
from parser_typeclasses.record_a import RecordTypeA


class TestResponse(unittest.TestCase):
    bytes_stream = b'da0481800001000200000000076d6f7a696c6c610e636c6f7564666c6172652d646e7303636f6d0000010001c00c00010001000000640004ac402904c00c00010001000000640004a29f3d04'
    parsed_packet = DNSPacketParser(bytes_stream)

    def test_bytes(self):
        dns_config: DNSConfig = DNSConfig()
        dns_config.ID = 55812
        dns_config.QR = 1
        dns_config.OP_CODE = 0
        dns_config.AA = 0
        dns_config.TTL = 0
        dns_config.RD = 1
        dns_config.RA = 1
        dns_config.Z = 0
        dns_config.RCODE = 0
        record_a : RecordTypeA = RecordTypeA()

        dns_config.QUERIES = []

