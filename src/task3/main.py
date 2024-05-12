import base64
import socket
import ssl

import os
import re

# TODO
# Все файлы лежат в отдельной папке
# Для работы клиента нужно 3 файла:
# Конфигурационный (Содержит адрес получателя, тему, имена файлов-аттачментов)
# Текстовый (В нем пользователь пишет письмо plain text на английском или русском языке)
# Файлы аттачменты

def request(socket, request: str) -> str:
    socket.send((request + '\n').encode())
    recv_data = socket.recv(65535).decode()
    return recv_data


def load_images(base_dir: str) -> list[str]:
    result = list()
    for path in os.listdir(base_dir):
        match os.path.isdir(path):
            case False: result.append(path)
            case True: result.append(*load_images(path))
    return result


def generate_boundary() -> str:
    return "my_bound"


host_addr = 'smtp.yandex.ru'
port = 465
user_name = "v.ruzne"
receivers = [""]
password = ""

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host_addr, port))
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        client = context.wrap_socket(client)
        print(client.recv(1024))

        print(request(client, f"EHLO {user_name}"))

        base64login = base64.b64encode(user_name.encode()).decode()
        base64password = base64.b64encode(password.encode()).decode()

        print(request(client, 'AUTH LOGIN'))
        print(request(client, base64login))
        print(request(client, base64password))

        print(request(client, f'MAIL FROM:{user_name}@yandex.ru'))
        print(request(client, f"RCPT TO:{user_name}@yandex.ru"))
        print(request(client, 'DATA'))

        # msg = ""
        # BOUNDARY = generate_boundary()
        #
        # with open("headers.txt") as file:
        #     msg += "".join(file.readlines()) + "\n"
        #
        # msg += "Content-Type: multipart/mixed;"
        # msg += f"boundary=\"{BOUNDARY}\"\n"
        # msg += "\n\n"
        #
        # msg += f"--{BOUNDARY}\n"
        # msg += "Content-Type: text/html\n\n"
        #
        # with open('body.txt') as file:
        #     for line in file.readlines():
        #         match re.match("^\.+$", line := line.strip("\n")):
        #             case re.Match(p=)
        #         line = line.strip("\n")
        #         if re.match("^\.+$", line):
        #             line += "."
        #         msg += line + "\n"
        # msg += f"--{BOUNDARY}\n"
        #
        # msg += "Content-Disposition: attachment;\n"
        # msg += "\tfilename=\"cat.jpg\"\n"
        #
        # msg += "Content-Transfer-Encoding: base64\n"
        # msg += "Content-Type: image/jpeg;\n"
        # msg += "\tname=\"dog.jpg\"\n\n"
        #
        # with open("cat.jpg", "rb") as file:
        #     image = base64.b64encode(file.read()).decode("utf-8")
        #     msg += image + "\n"
        # msg += f"--{BOUNDARY}--"
        # print(msg := msg + "\n.\n")
        # print(request(client, msg))

##TODO
##Обработка ошибок Сети
##MIME формат письма: присоединить картинки
##Заголовки письма: Subject, From и т. д.
##Корректное получение данных по сети
