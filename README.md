# API для поиска документов

## Технический стек

  

![](https://img.shields.io/badge/-Python-386e9d?style=for-the-badge&logo=Python&logoColor=ffd241&) ![FastAPI](https://img.shields.io/badge/FastAPI-323330?style=for-the-badge&logo=FastAPI) ![](https://img.shields.io/badge/-Elasticsearch-005571?style=for-the-badge&logo=Elasticsearch&logoColor=white) ![](https://img.shields.io/badge/-Kibana-005571?style=for-the-badge&logo=Kibana&logoColor=white) ![](https://img.shields.io/badge/-Postgresql-%232c3e50?style=for-the-badge&logo=Postgresql) ![](https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)

  

## Реализовано:

1. Сервис принимает на вход произвольный текстовый запрос, ищет документы по тексту документа в индексе и возвращает первые 20 документов со всем полями БД, упорядоченные по дате создания.
2. Создание документы в одновременно в БД и в индексе.
3. При создании документы с новыми рубриками, они создаются автоматически.
4. Удаление документов из БД и индекса по полю `id`.
5. Поднят сервис kibana.

## Архитектура:

Монолит

Разделение на слои:

- core (entities + usercases)

- adapters(infrastructure +presentation)

В ядре находятся обработчики бизнес логики, модели предметной области и протоколы, которые реализованы на слое adapters.

Такой подход дает удобство тестирования, и уменьшения зависимостей от реализаций.  

## Запуск

### В докер-контейнерах.

1. Клонировать репозиторий.

```
~$ git clone https://github.com/DeNeMiX83/search_by_document_texts
```

2. Создать .env в директории deploy на примере .env.dev.example и экспортировать ENV. **_НЕ ЗАБУДЬТЕ ПОМЕНЯТЬ ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ НА СВОИ!!!_**

```
~$ cd deploy && mv .env.dev.example .env.dev && export ENV=1
```

3. Собрать контейнеры.

```
~$ make compose-build
```

4. Поднять контейнеры.

```
~$ make compose-up
```

5. Создать индексы elasticsearch
```
~$ docker exec -it search_by_document_texts_backend bash
root@docer_id:/# make es-create-indexs
```

6. Загрузить тестовые данные
```
~$ docker exec -it search_by_document_texts_backend bash
root@docer_id:/# make dump_data
```
  
### На сервере.

.env из .env.dev.example, ENV экспортировать не нужно