# RAG
Вот ряд проектов, которые я считаю целесообразным изучить на данных момент.

- [Cognita](https://github.com/truefoundry/cognita)
- [RAGFlow](https://github.com/infiniflow/ragflow)
- [Quivr](https://github.com/QuivrHQ/quivr)
- [Dify](https://github.com/langgenius/dify)

Запуск локально: 
- https://hub.docker.com/r/ollama/ollama
- https://docs.docker.com/compose/gpu-support/

```bash
docker compose up
docker exec ollama ollama pull bambucha/saiga-llama3
```

```bash
# Для использования elasticsearch 
docker compose --profile elastic up
```

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

## Развертывание на Proxmox

```bash
vi /etc/apt/sources.list
```
```
deb http://ftp.debian.org/debian bookworm main contrib
deb http://ftp.debian.org/debian bookworm-updates main contrib

# Proxmox VE pve-no-subscription repository provided by proxmox.com,
# NOT recommended for production use
deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription

# security updates
deb http://security.debian.org/debian-security bookworm-security main contrib
``` 
```bash
vi /etc/apt/sources.list.d/ceph.list
```
```
# deb https://enterprise.proxmox.com/debian/ceph-quincy bookworm enterprise
```
```bash
vi /etc/apt/sources.list.d/pve-enterprise.list
```
```
# deb https://enterprise.proxmox.com/debian/pve bookworm pve-enterprise
```
```bash
apt-get update
apt-get upgrade 
cd  /var/lib/vz/template/iso 
wget https://mirror.linux-ia64.org/ubuntu-releases/24.04/ubuntu-24.04-live-server-amd64.iso
```

#### Сервисы

| Сервис                 | min требования             | Оптимально                      | .                                           | 
|------------------------|----------------------------|---------------------------------|---------------------------------------------|
| БД Postgres            | 1 CPU, 2 GB RAM, 3 GB disk | 4 CPU, 4 GB RAM, 32 GB disk     |                                             |
| FastAPI server с mongo | 2 CPU, 4 GB RAM, 3 GB disk | 4 CPU, 4 GB RAM, 10 GB disk     |                                             |
| Qdrant                 | 4 GB RAM                   | (4 CPU), 4 GB RAM, (32 GB disk) | 1e6 векторов по 512 с фактором репликации 2 | 


#### Postgres

```bash
# установить при установке ubuntu и обновить
sudo apt install --upgrade postgresql
```

#### Qdrant

```bash
sudo -s 
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
reboot
rustc --version

apt-get install -y git mold
apt-get install -y pkg-config gcc g++ libc6-dev libunwind-dev
apt-get install -y --no-install-recommends ca-certificates tzdata libunwind8
git clone https://github.com/qdrant/qdrant
cd qdrant
cargo build --release --bin qdrant
vi /lib/systemd/system/qdrant.service
```
```
[Unit]
Description=Qdrant vector DB

[Service]
ExecStart=~/qdrant/tools/entrypoint.sh
User=root

[Install]
WantedBy=multi-user.target 
```
```bash
systemctl start qdrant.service
systemctl stop qdrant.service
systemctl enable qdrant.service
```

#### FastAPI

Для mongo при создании ВМ в proxmox при выборе CPU нужен `home`, в остальных случаях можно `kvm64`
Установка `MongoDB`
```bash
sudo apt-get install gnupg curl
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo vi /etc/mongod.conf
sudo systemctl start mongod
sudo systemctl enable mongod
sudo systemctl status mongod
```


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

/* Зависит от размера модели
- https://developer.nvidia.com/blog/deploying-retrieval-augmented-generation-applications-on-nvidia-gh200-delivers-accelerated-performance/