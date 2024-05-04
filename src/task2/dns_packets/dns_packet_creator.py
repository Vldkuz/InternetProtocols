"""
Класс для формирования днс пакета
"""
from config_dns import DNSConfig
from creator_exception import CreatorException
from record_a import RecordTypeA
from record_aaaa import RecordTypeAAAA
from utils import TYPE_RECORD_BITS_OFFSET, CLASS_RECORD_BITS_OFFSET

BIN_OFFSET = 2
MAX_ID = 65535
ID_SIZE = 16
OP_CODE_SIZE = 4
Z_SIZE = 3
RCODE_SIZE = 4
QDCOUNT = ANCOUNT = NSCOUNT = ARCOUNT = 16
MAX_Z = 7
QR_AA_TC_RD_RA_VALUES = [0, 1]
OP_VALUES = [0, 1, 2]
RCODE_VALUES = [0, 1, 2, 3, 4, 5]
ZIPPED_LABEL_SIZE = 14
SIMPLE_LABEL_SIZE = 6
CH_SIZE = 8
HEADER_SIZE = 96
SIMPLE_LABEL = '00'
ZIPPED_LABEL = '11'
NAME_SPLITTER = '.'
TERMINATORS_NULL = '00'
CODEC = 'utf-8'

MAPPER_INVERSE_TYPE_RECORD = {'A': 1, 'NS': 2, 'CNAME': 5, 'SOA': 6, 'PTR': 12, 'MX': 15, 'TXT': 16, 'AAAA': 28,
                              'ANY': 255}
MAPPER_INVERSE_CLASS_RECORD = {'IN': 1, 'CS': 2, 'CH': 3, 'HS': 4}


def get_bin_section(name: str) -> str:
    bin_name = ''
    for char in name:
        bin_name += bin(ord(char))[BIN_OFFSET:].zfill(CH_SIZE)
    return bin_name


def convert_record_to_bits(record: RecordTypeA or RecordTypeAAAA, names_minder: dict, init_seek: int) -> tuple[str, int]:
    sections = qname.split(NAME_SPLITTER)
    last_is_zipped = False
    seek = init_seek
    query_bits = ""

    for section in sections:
        if section in names_minder:
            label = ZIPPED_LABEL
            pointer = bin(names_minder[section])[BIN_OFFSET:].zfill(ZIPPED_LABEL_SIZE)
            seek += len(label) + len(pointer)
            query_bits += label + pointer
            last_is_zipped = True
        else:
            names_minder[section] = seek
            label = SIMPLE_LABEL
            size_name = bin(len(section))[BIN_OFFSET:].zfill(SIMPLE_LABEL_SIZE)
            encoded_name = get_bin_section(section)
            query_bits += label + size_name + encoded_name
            seek += len(size_name) + len(label) + len(encoded_name)
            last_is_zipped = False

    if not last_is_zipped:
        query_bits += TERMINATORS_NULL

    return query_bits, seek


class DNSCreator:
    def __init__(self, config: DNSConfig):
        self._config = config

    def __bytes__(self):
        bytes_packet = ''  # Здесь все в бинарку сложим и отпарсим потом hex

        """
        Здесь нужно завести какой-то словарь для использования потом сжатых меток
        ключ - имя, значение - указатель, куда сместится от начала пакета
        """

        names_minder = {}

        if self._config.ID > MAX_ID:
            raise CreatorException(f"ID больше максимального допустимого id (65535): {self._config.ID}")

        id_bits: str = bin(self._config.ID)[BIN_OFFSET:].zfill(16)

        if self._config.QR not in QR_AA_TC_RD_RA_VALUES:
            raise CreatorException(
                f'Поле не может быть однозначно идентифицировано как запрос или ответ (0, 1): {self._config.QR}')

        qr_bits: str = str(self._config.QR)

        if self._config.OP_CODE not in OP_VALUES:
            raise CreatorException(
                f'Поле не может быть однозначно идентифицировано как код запроса (0, 1, 2): {self._config.OP_CODE}')

        op_code_bits: str = bin(self._config.OP_CODE)[BIN_OFFSET:].zfill(OP_CODE_SIZE)

        if self._config.AA not in QR_AA_TC_RD_RA_VALUES:
            raise CreatorException(
                f'Поле не может быть однозначно идентифицировано как код авторитета (0, 1): {self._config.AA}')

        aa_bits: str = str(self._config.AA)

        if self._config.TC not in QR_AA_TC_RD_RA_VALUES:
            raise CreatorException(
                f'Поле не может быть однозначно идентифицировано как код обрезки пакета (0, 1): {self._config.TC}')

        tc_bits: str = str(self._config.TC)

        if self._config.RD not in QR_AA_TC_RD_RA_VALUES:
            raise CreatorException(
                f'Поле не может быть однозначно идентифицировано как код желания рекурсии (0, 1): {self._config.RD}')

        rd_bits: str = str(self._config.RD)

        if self._config.RA not in QR_AA_TC_RD_RA_VALUES:
            raise CreatorException(
                f'Поле не может быть однозначно идентифицировано как код возможности рекурсии (0, 1): {self._config.RA}')

        ra_bits: str = str(self._config.RA)

        if self._config.Z > MAX_Z:
            raise CreatorException(
                f"Значение в поле не может быть больше 7 из-за размерности поля в 3 бита {self._config.Z}")

        z_bits: str = bin(self._config.Z)[BIN_OFFSET:].zfill(Z_SIZE)

        if self._config.RCODE not in RCODE_VALUES:
            raise CreatorException(
                f"Поле не может быть однозначно идентифицировано как статус выполнения запроса (0, 1, 2, 3, 4, 5) {self._config.RCODE}")

        rcode_bits: str = bin(self._config.RCODE)[BIN_OFFSET:].zfill(RCODE_SIZE)

        qdcount_bits: str = bin(self._config.QDCOUNT)[BIN_OFFSET:].zfill(QDCOUNT)
        ancount_bits: str = bin(self._config.ANCOUNT)[BIN_OFFSET:].zfill(ANCOUNT)
        nscount_bits: str = bin(self._config.NSCOUNT)[BIN_OFFSET:].zfill(NSCOUNT)
        arcount_bits: str = bin(self._config.ARCOUNT)[BIN_OFFSET:].zfill(ARCOUNT)

        if len(self._config.QUERIES) != self._config.QDCOUNT:
            raise CreatorException(
                f'Несоответствие секции запросов количеству записей в секции запросов заголовка {self._config.QDCOUNT}, {len(self._config.QUERIES)}')

        query_bits: str = ""

        seek = HEADER_SIZE

        for record in self._config.QUERIES:
            encoded_qname = convert_record_to_bits(record.qname, names_minder, seek)

            seek = encoded_qname[1]
            query_bits += encoded_qname[0]

            type_record_bits = bin(MAPPER_INVERSE_TYPE_RECORD[record.type_record])[BIN_OFFSET:].zfill(TYPE_RECORD_BITS_OFFSET)
            class_record_bits = bin(MAPPER_INVERSE_CLASS_RECORD[record.class_record])[BIN_OFFSET:].zfill(CLASS_RECORD_BITS_OFFSET)
            query_bits += type_record_bits + class_record_bits
            seek += len(type_record_bits) + len(class_record_bits)

        answer_bits: str = ""

        for answer in self._config.ANSWERS:
            encoded_qname = convert_record_to_bits(answer.qname, names_minder, seek)

            seek = encoded_qname[1]



        """Здесь собираем пакет обратно в байты"""
