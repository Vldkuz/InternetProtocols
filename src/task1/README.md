# Задача 1
Формулировка задачи: На вход утилиты ipv4/доменное имя. Делает трассировку до этого хоста, в том смысле, что описывает списком через какие автономные системы проходит.

**Особенности работы скрипта**:

* Требует прав суперпользователя, поскольку используется зарезервированный 43 порт.
* Адреса, по которым нет AS - нет информации у регистраторов об их AS.

## Запуск под Linux:

1. Перейдите в директорию **EthernetProtocols/src/task1**:

```
cd EthernetProtocols/src/task1
```

2. Создайте виртуальное окружение и установите зависимости:

```
python -m venv .venv; source .venv/bin/activate; pip install -r requirements.txt
```

3. Запустите файл с правами суперпользователя:

`sudo python whoistrace.py google.com`


## Запуск под Windows:

1. Перейдите в директорию **EthernetProtocols\src\task1**:

```
cd EthernetProtocols\src\task1
```

2. Создайте виртуальное окружение и установите зависимости:

```
python -m venv .venv && source .venv\Scripts\activate.bat && pip install -r requirements.txt
```

3. Запустите консоль от имени администратора:

`python whoistrace.py google.com`


## Пример вывода 
    +-----------------+---------+---------+-------------------------------------+
    |        IP       |    AS   | Country |             Description             |
    +-----------------+---------+---------+-------------------------------------+
    |   192.168.1.1   |         |         |                                     |
    |   91.191.249.1  | AS12668 |    RU   | MiraLogic Telecommunication Systems |
    |  92.242.29.194  | AS12668 |    RU   | MiraLogic Telecommunication Systems |
    |  5.140.215.238  | AS12389 |    RU   |         Rostelecom networks         |
    |  5.140.215.237  | AS12389 |    RU   |         Rostelecom networks         |
    |  95.167.92.190  | AS12389 |    RU   |           ROSTELECOM NETS           |
    |   72.14.209.89  |         |         |                                     |
    | 108.170.250.129 | AS15169 |    US   |              Google LLC             |
    | 108.170.250.146 | AS15169 |    US   |              Google LLC             |
    | 142.251.237.156 | AS15169 |    US   |              Google LLC             |
    | 142.251.237.144 | AS15169 |    US   |              Google LLC             |
    | 142.250.232.179 | AS15169 |    US   |              Google LLC             |
    |  142.251.1.100  | AS15169 |    US   |              Google LLC             |
    +-----------------+---------+---------+-------------------------------------+

