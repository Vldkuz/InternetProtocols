import re
from typing import Optional

EXTRA_POINT_REGEXP = re.compile(r"^\.+$")


class BodyPart:
    def __init__(self, boundary: str, body: Optional[str] = None) -> None:
        self._boundary = boundary
        self._body = f"<div>{body}</div>"

    def build(self) -> str:
        if self._body is None:
            return ""

        body_part = [
            f"--{self._boundary}\n",
            "Content-Type: text/html\n\n"
        ]

        for line in self._body.split("\n"):
            if EXTRA_POINT_REGEXP.match(line):
                line += "."
            body_part.append(f"{line}\n")

        return "".join(body_part)
