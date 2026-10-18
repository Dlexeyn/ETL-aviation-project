# Aviation ETL

ETL-проект для извлечения, преобразования и загрузки данных об авиационных инцидентах из CSV-файла в PostgreSQL с использованием Python, pandas и Docker Compose.

## Технологии

- **Python 3.12** — реализация ETL-процесса.
- **pandas** — обработка и проверка данных.
- **PostgreSQL 17** — хранение обработанных данных.
- **psycopg2** — подключение к базе данных.
- **Docker Compose** — запуск и управление контейнерами.

## Структура проекта

```text
aviation-etl/
├── compose.yaml
├── Dockerfile
├── requirements.txt
├── .dockerignore
├── .env
├── etl.py
├── data/
│   └── incidents.csv
└── output/
    └── rejected_incidents.csv
```

## Подготовка и запуск

1. Установите Docker и Docker Compose.
2. Поместите исходный файл `incidents.csv` в каталог `data/`.
3. Настройте параметры подключения к PostgreSQL в `.env`. Задайте собственный пароль вместо `change_this_password`.
4. Запустите PostgreSQL:

   ```bash
   docker compose up -d postgres
   ```

5. Выполните ETL-процесс:

   ```bash
   docker compose --profile tools run --build --rm etl
   ```

## Этапы ETL

- **Extract** — чтение исходного CSV-файла.
- **Transform** — преобразование типов, проверка обязательных полей, уникальности идентификаторов и согласованности значений.
- **Load** — загрузка корректных записей в таблицу `incidents` базы данных PostgreSQL.

Записи, не прошедшие проверку качества, сохраняются в `output/rejected_incidents.csv`. Повторный запуск не приводит к дублированию записей с одинаковым `incident_id`.

## Проверка результата

Количество записей в таблице:

```bash
docker compose exec postgres psql -U postgres -d