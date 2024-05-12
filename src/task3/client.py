from __future__ import annotations

import os
import ssl
import base64
import socket

from src.task3.messages.message import Message


class SMTPClient:
    def __init__(self, login: str, passwd: str, host_addr: str, port: int) -> None:
        self._client = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )

        self._login = login
        self._passwd = passwd
        self._client = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2).wrap_socket(self._client)
        self._client.connect((host_addr, port))
        self._client.recv(1024)

    def auth_client(self) -> SMTPClient:
        self._send_request(f"EHLO {self._login}")

        base64login = base64.b64encode(self._login.encode())
        base64password = base64.b64encode(self._passwd.encode())

        self._send_request("AUTH LOGIN")
        self._send_request(base64login.decode())
        response = self._send_request(base64password.decode())

        if not response.startswith("235"):
            raise ConnectionError

        return self

    def check_receivers(self, receivers: list[str]) -> SMTPClient:
        for receiver in receivers:
            response = self._send_request(f"RCPT TO:{receiver}")
            if not response.startswith("250"):
                raise ValueError(receiver)
        return self

    def check_sender(self) -> SMTPClient:
        response = self._send_request(f"MAIL FROM:{os.getenv('LOGIN')}@yandex.ru")
        if not response.startswith("250"):
            raise ValueError(self._login)

        return self

    def send_message(self, message: Message) -> str:
        self.check_sender()
        message_text = message.build()
        self.check_receivers(message.receivers)

        self._send_request("DATA")
        return self._send_request(message_text)

    def _send_request(self, data: str) -> str:
        self._client.send(f'{data}\n'.encode())
        return self._client.recv(1024).decode()

    def __del__(self) -> None:
        self._client.close()
