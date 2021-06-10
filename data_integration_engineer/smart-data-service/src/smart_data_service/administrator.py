import logging

from pydantic import Json, ValidationError

import src.smart_data_service.schemas as schemas
from src.smart_data_service.db_operations import DbSession
from src.smart_data_service.messaging import MessageProcessor


def on_message(message: Json, session: DbSession) -> None:
    """Whenever a new message from broker: validate and add to the database"""
    try:
        smart_data = schemas.SmartData.from_json(message)
        session.add_smart_data(smart_data)
        logging.info("Received: %s", smart_data)
    except ValidationError as exc:
        logging.error("ERROR: Invalid schema: %s", exc)


with MessageProcessor() as processor, DbSession() as db_session:
    processor.consume(on_message, db_session)
