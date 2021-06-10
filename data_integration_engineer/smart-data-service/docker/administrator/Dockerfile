FROM python:3.9.5-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY ./docker/administrator /tmp/requirements
RUN pip3 install --no-cache-dir -r /tmp/requirements/requirements.txt


COPY ././src /app/src
ENV PYTHONPATH "${PYTHONPATH}:/app"
WORKDIR /app

ENTRYPOINT ["python", "src/smart_data_service/administrator.py"]