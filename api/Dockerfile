FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    docker.io procps curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Скачиваем docker-compose v2 как отдельный бинарник
RUN curl -fsSL https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-linux-x86_64 \
    -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
