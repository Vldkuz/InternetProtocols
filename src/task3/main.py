import json
import os.path
from typing import Any

from dotenv import load_dotenv

from src.task3.client import SMTPClient
from src.task3.messages.message import MessageBuilder

MAIL_DIR = 'mail'
JSON_NAME = 'mail.json'

LOGIN = os.getenv('LOGIN')
PASSWD = os.getenv('PASSWORD')
HOST_ADDR = os.getenv('HOST_ADDR')
PORT = os.getenv('PORT') or 465

if __name__ == '__main__':
    load_dotenv()
    path = os.path.join(MAIL_DIR, JSON_NAME)

    with open(path, "r") as file:
        mail_data: dict[str, Any] = json.load(file)
        message = (MessageBuilder.builder()
                   .set_body(mail_data.get("body"))
                   .set_subject(mail_data.get("subject"))
                   .add_receivers(*mail_data.get("receivers"))
                   .add_attachments(*mail_data.get("attachments")))

        response = (SMTPClient(LOGIN, PASSWD, HOST_ADDR, int(PORT)).auth_client()
                    .send_message(message.build_message()))
