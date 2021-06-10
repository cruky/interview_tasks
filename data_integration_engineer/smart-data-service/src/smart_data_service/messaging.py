from typing import Callable

import pika
from pika import BlockingConnection, URLParameters
from pika.adapters.blocking_connection import BlockingChannel

from src.smart_data_service.config import (
    AMQP_URL,
    SMART_METER_TO_ADMIN_EXCHANGE,
    SMART_METER_TO_ADMIN_QUEUE,
    SMART_METER_TO_ADMIN_ROUTING_KEY,
)
from src.smart_data_service.db_operations import DbSession


class RabbitConnection:
    """
    RabbitMQ connector
    """

    def __init__(self, url, queue, exchange, routing_key):
        self._url: str = url
        self.params: URLParameters = pika.URLParameters(self._url)
        self.connection: BlockingConnection
        self.channel: BlockingChannel
        self.routing_key: str = routing_key
        self.queue: str = queue
        self.exchange: str = exchange

    def init(self) -> None:
        """Initialize blocking connection and channel"""
        self.connection = pika.BlockingConnection(parameters=self.params)
        self.channel = self.connection.channel()  # start a channel
        self.channel.queue_declare(queue=self.queue, auto_delete=False, durable=False)
        self.channel.exchange_declare(exchange=self.exchange, auto_delete=False, durable=False)
        self.channel.queue_bind(queue=self.queue, exchange=self.exchange, routing_key=self.routing_key)

    def publish(self, data: str) -> None:
        """Publish to the channel with the given exchange, routing key and body"""
        message = data.encode()
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.routing_key,
            body=message,
            properties=pika.BasicProperties(content_type="application/json"),
        )


class MessageProcessor:
    """
    Process messages with Pub-Sub pattern
    """

    def __init__(self):
        self.to_admin: RabbitConnection = RabbitConnection(
            url=AMQP_URL,
            queue=SMART_METER_TO_ADMIN_QUEUE,
            exchange=SMART_METER_TO_ADMIN_EXCHANGE,
            routing_key=SMART_METER_TO_ADMIN_ROUTING_KEY,
        )

    def __enter__(self):
        self.to_admin.init()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.to_admin.channel.cancel()
        self.to_admin.channel.close()
        self.to_admin.connection.close()

    def publish(self, data: str) -> None:
        """Publish a message to the broker"""
        self.to_admin.publish(data)

    def consume(self, on_message: Callable[[str, DbSession], None], session: DbSession) -> None:
        """Blocking consumption of a queue.
        This method is a generator that yields each message as a tuple of:
        method, properties, and body.
        :param on_message: when message run function on_message.
        :param session: db session.
        body: message in bytes
        """
        for method_frame, _, body in self.to_admin.channel.consume(self.to_admin.queue):
            on_message(body.decode(), session)
            # Acknowledge the message
            self.to_admin.channel.basic_ack(method_frame.delivery_tag)
