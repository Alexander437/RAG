# RAG
Вот ряд проектов, которые я считаю целесообразным изучить на данных момент.

- [Cognita](https://github.com/truefoundry/cognita)
- [RAGFlow](https://github.com/infiniflow/ragflow)
- [Quivr](https://github.com/QuivrHQ/quivr)
- [Dify](https://github.com/langgenius/dify)

## Server requirements

При использовании API (ChatGPT, GigaChat и др.), 
я ориентируюсь на требования, указанные в https://github.com/infiniflow/ragflow (но больше cores и ram):

CPU >= 8 cores с SMT
RAM >= 32 GB
Disk >= 50 GB

Дополнительно для индексирования текстов потребуется видеокарта Nvidia емкостью не менее 8 GB или возможно
использование API. Считаю эти требования минимально необходимыми для развертывания и тестирования
системы.

При запуске в `docker compose`:
добавить или обновить значение `vm.max_map_count` в файле /etc/sysctl.conf:

```bash
vm.max_map_count=262144
```

## Links

* https://github.com/truefoundry/rag-blog
* https://www.linkedin.com/pulse/what-hardware-do-you-need-rag-genai-vasudev-lal-cf4vc

## Tests

```bash
pytest tests/dataloaders
```

## Additional

`python==3.10.13`

Расчеты (будут заполнены после проведения пробного запуска и мониторинга приложения):

|                        | Процессор | ОЗУ     | CUDA (Видеокарта Nvidia) | Жесткий диск | Сеть | Ссылка                            |
|------------------------|-----------|---------|--------------------------|--------------|------|-----------------------------------|
| векторная БД           |
| поиск текстов          |
| работа LLM             |           | 8-30 Gb | 5-50 GB и более *        | 5-50 GB      |      | https://github.com/ollama/ollama  |
| взаимодействие с польз |
| Всего                  |

- для [SingleStore в docker](https://www.singlestore.com/blog/spin-up-a-memsql-cluster-on-docker-desktop-in-10-minutes/):
8 GB RAM, 4 cores CPU
- 
/** SingleStore Бесплатно до четырех узлов с 32 ГБ ОЗУ каждый и при поддержке сообщества.

/* Зависит от размера модели
- https://developer.nvidia.com/blog/deploying-retrieval-augmented-generation-applications-on-nvidia-gh200-delivers-accelerated-performance/