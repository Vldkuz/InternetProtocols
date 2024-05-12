from __future__ import annotations

import os
from random import randint
from typing import Any, Optional

from messages.head_part import HeadPart
from messages.body_part import BodyPart
from messages.attach_part import AttachPart


class Message:
    def __init__(self, params: dict[str, Any]) -> None:
        self._boundary = self._generate_boundary()
        self.login = os.getenv('LOGIN')
        self._head_part = self._create_head(params)
        self._body_part = self._create_body(params)
        self._attachment_part = self._create_attachments(params)

    @property
    def receivers(self) -> list[str]:
        return self._head_part.receivers

    def build(self) -> str:
        return "".join([
            self._head_part.build(),
            self._body_part.build(),
            self._attachment_part.build(),
            f"--{self._boundary}--\n.\n",
        ])

    def _create_head(self, params: dict[str, Any]) -> HeadPart:
        return HeadPart(
            self._boundary,
            params.get("receivers"),
            params.get("subject")
        )

    def _create_body(self, params: dict[str, Any]) -> BodyPart:
        return BodyPart(
            self._boundary,
            params.get("body")
        )

    def _create_attachments(self, params: dict[str, Any]) -> AttachPart:
        return AttachPart(
            self._boundary,
            params.get("attachments")
        )

    @classmethod
    def _generate_boundary(cls) -> str:
        return f"bound.{''.join([chr(randint(100, 120)) for _ in range(10)])}"


class MessageBuilder:
    def __init__(self):
        self._subject = str()
        self._receivers: list[str] = []
        self._body: Optional[str] = None
        self._attachments: list[str] = []

    @staticmethod
    def builder() -> MessageBuilder:
        return MessageBuilder()

    def build_message(self) -> Message:
        return Message({
            "body": self._body,
            "subject": self._subject,
            "receivers": self._receivers,
            "attachments": self._attachments,
        })

    def set_subject(self, new_subject: str) -> MessageBuilder:
        self._subject = new_subject
        return self

    def set_body(self, new_body: str) -> MessageBuilder:
        self._body = new_body
        return self

    def add_receivers(self, *receivers: str) -> MessageBuilder:
        self._receivers += list(receivers)
        return self

    def add_attachments(self, *attachments: str) -> MessageBuilder:
        self._attachments += list(attachments)
        return self
