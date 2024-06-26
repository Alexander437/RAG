# RAG
Вот ряд проектов, которые я считаю целесообразным изучить на данных момент.

- [Cognita](https://github.com/truefoundry/cognita)
- [RAGFlow](https://github.com/infiniflow/ragflow)
- [Quivr](https://github.com/QuivrHQ/quivr)
- [Dify](https://github.com/langgenius/dify)


## Проблемы

* включить авторизацию в вызовы api и сделать уведомления на почту
* Добавить OCR для чтения pdf и фото
* Возможно нужен celery?
* Добавить в `internal` проверку доступности

## Local RUN

Добавить документы в коллекцию:

POST `/collections/ingest` -> в аргументах должен быть абсолютный путь к файлу

ИЛИ

1. Редактировать файл `volumes/backend/metadata.yaml`
2. `docker compose up`
3. `python ingest.py`

## Server requirements

При использовании API (ChatGPT, GigaChat и др.), 
я ориентируюсь на требования, указанные в https://github.com/infiniflow/ragflow (но больше cores и ram):

CPU >= 8 cores с SMT
RAM >= 32 GB
Disk >= 50 GB

Дополнительно для индексирования текстов потребуется видеокарта Nvidia емкостью не менее 8 GB или возможно
использование API. Считаю эти требования минимально необходимыми для развертывания и тестирования
системы.

## Links

* https://github.com/truefoundry/rag-blog
* https://www.linkedin.com/pulse/what-hardware-do-you-need-rag-genai-vasudev-lal-cf4vc


## Additional

`python==3.10.13`