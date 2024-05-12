import base64
import os
from typing import Optional

import magic

MAIL_DIR = 'messages'
ATTACHMENTS_DIR = 'attachments'


class AttachPart:
    def __init__(self, boundary: str, attachments: Optional[list[str]] = None) -> None:
        self._boundary = boundary
        self._attachments = attachments or []

    def build(self) -> str:
        attach_part = []

        for filename in self._attachments:
            path = os.path.join(MAIL_DIR, ATTACHMENTS_DIR, filename)

            if not os.path.isfile(path):
                print(f"Error on file: {filename}")
                continue

            attach_part.append(f"--{self._boundary}\n")
            attach_part.append(f"Content-Disposition: attachment;\n")
            attach_part.append(f"\tfilename=\"{filename}\"\n")

            mime_type = magic.from_file(path, mime=True)

            attach_part.append("Content-Transfer-Encoding: base64\n")
            attach_part.append(f"Content-Type: {mime_type};\n")
            attach_part.append(f"\tname=\"{filename}\"\n\n")

            with open(path, "rb") as file:
                attach = base64.b64encode(file.read()).decode()
                attach_part.append(f'{attach}\n')

        return "".join(attach_part)



