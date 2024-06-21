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
apt-get update && apt-get upgrade -y
cd  /var/lib/vz/template/iso 
wget https://mirror.linux-ia64.org/ubuntu-releases/24.04/ubuntu-24.04-live-server-amd64.iso
```

### Сервисы

| Сервис                 | min требования              | Оптимально                      | .                                           | 
|------------------------|-----------------------------|---------------------------------|---------------------------------------------|
| БД Postgres            | 1 CPU, 2 GB RAM, 3 GB disk  | 4 CPU, 4 GB RAM, 32 GB disk     |                                             |
| FastAPI server с mongo | 2 CPU, 4 GB RAM, 75 GB disk | 4 CPU, 4 GB RAM, 100 GB disk    |                                             |
| Qdrant                 | 4 GB RAM                    | (4 CPU), 8 GB RAM, (32 GB disk) | 1e6 векторов по 512 с фактором репликации 2 | 
| Ollama                 | 32 GB disk                  |                                 |

### Postgres

```bash
# установить при установке ubuntu и обновить
sudo apt install --upgrade postgresql
curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor -o /usr/share/keyrings/packages-pgadmin-org.gpg
sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
sudo apt install pgadmin4-web
sudo /usr/pgadmin4/bin/setup-web.sh
# http://{postgres_host}/pgadmin4
# Query tool
# INSERT INTO role VALUES (1, 'user', null);
sudo vi /etc/postgresql/16/main/postgresql.conf
```
``` 
listen_addresses = '*'
```
```bash
sudo vi /etc/postgresql/16/main/pg_hba.conf
```
```
... 
host all all 0.0.0.0/0 md5
``` 
```bash
systemctl restart postgresql
sudo -u postgres psql
CREATE USER auth WITH PASSWORD 'jw8s0F4' CREATEDB;
CREATE DATABASE auth OWNER auth;
```

### Qdrant

```bash
sudo apt-get install -y jq unzip
sudo apt-get install -y --no-install-recommends ca-certificates tzdata libunwind8
git clone https://github.com/qdrant/qdrant
cd qdrant
./tools/sync-web-ui.sh
mkdir build
```
Скопировать в build ~/qdrant/static и скачать сюда саму сборку

Создать файл build/config/config.yaml, все пути заменить на абсолютные
```
storage:
    on_disk_payload: true
    storage_path: /home/qdrant/build/storage
```
Скопировать ~/qdrant/tools/entrypoint.sh в build как start.sh и запускать им.
Все пути заменить на абсолютные.

```bash
sudo vi /lib/systemd/system/qdrant.service
```
```
[Unit]
Description=Qdrant vector DB

[Service]
ExecStart=/home/qdrant/build/start.sh
User=root
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload
sudo systemctl enable qdrant.service --now
sudo systemctl status qdrant.service
```

### Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull bambucha/saiga-llama3

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

### FastAPI

Для mongodb нужно выбирать тип процессора `host` и disk      на `local/lvm`
```bash
sudo apt-get install gnupg curl git
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y mongodb-org
sudo vi /etc/mongod.conf
sudo systemctl enable mongod --now
```

```bash
sudo apt-get install python3-pip python3.12-venv -y
python3 -m venv rag_env
source rag_env/bin/activate
pip install -r backend/requirements.txt
nano .env
```