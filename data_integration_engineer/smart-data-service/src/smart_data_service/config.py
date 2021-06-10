import logging
import os

RABBIT_MQ_HOST: str = os.environ.get("RABBIT_MQ_HOST", "localhost")
RABBIT_MQ_PORT: str = os.environ.get("RABBIT_MQ_PORT", "5672")
RABBIT_MQ_USER: str = os.environ.get("RABBIT_MQ_USER", "admin")
RABBIT_MQ_PASS: str = os.environ.get("RABBIT_MQ_PASS", "admin")
AMQP_URL: str = f"amqp://{RABBIT_MQ_USER}:{RABBIT_MQ_PASS}@{RABBIT_MQ_HOST}:{RABBIT_MQ_PORT}/"
SMART_METER_TO_ADMIN_QUEUE: str = "smart_meter.administrator.queue"
SMART_METER_TO_ADMIN_EXCHANGE: str = " smart_meter.administrator.exchange.direct"
SMART_METER_TO_ADMIN_ROUTING_KEY: str = "smart_meter.message"

POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT", "8080")
POSTGRES_USER: str = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD", "postgres")
POSTGRES_DATABASE: str = os.environ.get("POSTGRES_DATABASE", "smart_data")
DB_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

API_PORT: int = int(os.environ.get("PORT", "5000"))

DATETIME_REGEX: str = r"^\d{4}-\d{1,2}-\d{1,2}$"
TIME_STAMP_REGEX: str = r"^\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2}$"
READING_DURATION_DAYS: int = 1
TIME_INTERVALS_MINUTES: int = 15
# READING_DURATION_DAYS should be n(int)*TIME_INTERVALS_MINUTES

FORMAT: str = "%(asctime)s,  %(message)s"
logging.basicConfig(level=logging.ERROR, format=FORMAT)
