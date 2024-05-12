import base64
import os
import re
from typing import Optional

RE_RUSSIAN_LANGUAGE = re.compile("[а-яА-ЯёЁ]")


class HeadPart:
    def __init__(self, boundary: str, receivers: list[str], login: str, subject: Optional[str] = None) -> None:
        self._boundary = boundary
        self._receivers = receivers
        self._subject = self._normalize_subject(subject)
        self._login = login

        if not len(self._receivers):
            raise ValueError("No mail receivers found")

    @property
    def receivers(self) -> list[str]:
        return self._receivers

    def build(self) -> str:

        message_part = [
            f"From: <{self._login}@yandex.ru>\n",
            f"To: " + ",\n\t".join(map(lambda x: f'{x}', self._receivers)) + "\n",
        ]

        if self._subject is not None:
            message_part.append(f"Subject: {self._subject}\n")

        message_part += [
            f"MIME-Version: 1.0\n",
            f"Content-Type: multipart/mixed;boundary=\"{self._boundary}\"\n\n\n",
        ]

        return "".join(message_part)

    @staticmethod
    def _normalize_subject(subject: str) -> str:
        if subject and not RE_RUSSIAN_LANGUAGE.search(subject):
            return subject

        parts = []
        for i in range(0, len(subject), 30):
            part = subject[i:min(len(subject), i + 30)]
            base64part = base64.b64encode(part.encode()).decode()
            parts.append(f'=?utf-8?B?{base64part}?=')
        return "\n\t".join(parts)
