import json
import os.path
from typing import Any

from dotenv import load_dotenv

from smtp_client import SMTPClient
from messages.message import MessageBuilder

MAIL_DIR = 'mail'
JSON_NAME = 'mail.json'
CONFIGS_DIR = 'configs'

load_dotenv(dotenv_path=os.path.join(CONFIGS_DIR, '.env'))

LOGIN = os.getenv('LOGIN')
PASSWD = os.getenv('PASSWORD')
HOST_ADDR = os.getenv('HOST_ADDR')
PORT = os.getenv('PORT') or 465

if __name__ == '__main__':
    path = os.path.join(MAIL_DIR, JSON_NAME)

    with open(path, "r") as file:
        mail_data: dict[str, Any] = json.load(file)
        message = (MessageBuilder.builder()
                   .set_body(mail_data.get("body"))
                   .set_subject(mail_data.get("subject"))
                   .add_receivers(*mail_data.get("receivers"))
                   .add_attachments(*mail_data.get("attachments")))

        response = (SMTPClient().auth_client()
                    .send_message(message.build_message()))
