# Установка и запуск

1. Установка 
```pip3 install -r requirements.txt```


2. Запуск 
   - Запустить сервер Redis
   - Подключиться к PostgreSQL
   - В коде вставить свои данные для подключения к Redis и PostgreSQL
   - Запустить приложение:
     - через терминал: запуск из файла main.py```uvicorn main:app --reload```
     - из .py файла в PyCharm: ```запустить через файл pymain.py```


SQL Запросы находятся в файле custom_postgres_query.py

---

## Скрипт для создания базы данных PostgreSQL:

create table devices
(
    id       bigserial    not null
        constraint devices_pk
            primary key,
    dev_id   varchar(200) not null,
    dev_type varchar(120) not null
);

alter table devices
    owner to postgres;

create index devices_dev_id_dev_type_index
    on devices (dev_id, dev_type);

create table endpoints
(
    id        bigserial not null
        constraint endpoints_pk
            primary key,
    device_id integer
        constraint endpoints_devices_id_fk
            references devices
            on update cascade on delete cascade,
    comment   text
);

alter table endpoints
    owner to postgres;

---

## Тестовое задание

стек: aioredis, fastapi, asyncpg

Тестовое приложение должно подключатся к PostgreSQL и Redis и реализовать
следующие API:

1. Проверка анаграммы - принимает две строки, определяет, являются ли они анаграммами. 
Если являются - необходимо увеличить счетчик в Redis. 
Возвращает JSON - являются ли они анаграммами и счетчик из Redis.


2. Занести в базу данных 10 устройств (таблица devices), 
тип (dev_type) определяется случайно из списка: emeter, zigbee, lora, gsm. 
Поле dev_id - случайные 48 бит в hex-формате (MAC-адрес). 
К пяти устройствам из добавленных необходимо привязать endpoint (таблица endpoints). 
После записи необходимо возвращать HTTP код состояния 201.


3. В базе данных получить список всех устройств, которые не привязаны к
endpoint. Вернуть количество, сгруппированное по типам устройств.
