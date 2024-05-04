from record_answer import Answer
from record_query import Query


class DNSConfig:
    def __init__(self):
        self.ID = None
        self.QR = None
        self.OP_CODE = None
        self.AA = None
        self.TC = None
        self.RD = None
        self.RA = None
        self.Z = None
        self.RCODE = None
        self.QDCOUNT = None
        self.ANCOUNT = None
        self.NSCOUNT = None
        self.ARCOUNT = None
        self.QUERIES: list[Query] or None = None
        self.ANSWERS: list[Answer] or None = None
        self.AUTHORITY: list[Answer] or None = None
        self.ADDITIONAL: list[Answer] or None = None

