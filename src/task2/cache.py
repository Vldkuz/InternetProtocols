from __future__ import annotations

import json
import os.path
import re

from record_a import RecordTypeA
from record_aaaa import RecordTypeAAAA
from record_mx import RecordTypeMX
from record_ns import RecordTypeNS
from record_ptr import RecordTypePTR
from record_soa import RecordTypeSoa

FIRST = 0
SECOND = 1

reg_ip = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')


class Cache:
    def __init__(self):
        self.ip_to_name = {}
        self.name_to_ip = {}

    def push(self, key: str, type_record: str,
             info: RecordTypeA or RecordTypeAAAA or RecordTypeMX or RecordTypeNS or RecordTypePTR or RecordTypeSoa) -> None:
        if reg_ip.match(key):
            self.ip_to_name[key] = (type_record, info)
        else:
            self.name_to_ip[key] = (type_record, info)

    def clean(self) -> None:
        self.ip_to_name.clear()
        self.name_to_ip.clear()

    def get(self, key: str, type_record: str) -> None or str:
        value_key = self.ip_to_name.get(key) or self.name_to_ip.get(key)

        if value_key is None:
            return None

        record = value_key[FIRST]

        if record == type_record:
            return value_key[SECOND]

        return None

    def from_json(self, name: str):
        if not os.path.exists(name):
            file = open(name, 'w')
            file.close()

        with open(name, 'r') as file:
            data = json.load(file)

            self.ip_to_name = data[FIRST]
            self.name_to_ip = data[SECOND]

    def to_json(self, name: str):
        with open(name, 'w') as file:
            data = (self.ip_to_name, self.name_to_ip)
            json.dump(data, file, default=lambda x: x.__dict__)
