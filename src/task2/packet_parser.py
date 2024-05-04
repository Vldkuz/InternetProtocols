class DNSParser:
    """
    Типы записей DNS:
    A - домен -> IPv4 адрес - код 1 + +
    AAAA - домен -> IPv6 адрес - код 28 + +
    CNAME - домен -> поддомен - код 5 + +
    MX - домен -> доменное имя почтового сервера - код 15 + +
    TXT - домен -> Текстовая запись о домене - код 16 -
    NS - домен -> днс серверы домена - код 2 + +
    PTR - IP -> домен - код 12 + +
    SOA - домен -> запись зоны - код 6 + +
    """

    def __init__(self, bytes_stream: bytes):
        pass

    

