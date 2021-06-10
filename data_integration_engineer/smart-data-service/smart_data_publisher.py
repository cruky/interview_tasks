#!/usr/bin/env python

import json
import re
import time
from datetime import datetime, timedelta
from random import uniform
from typing import Generator, List

import click

from src.smart_data_service.config import DATETIME_REGEX, READING_DURATION_DAYS, TIME_INTERVALS_MINUTES
from src.smart_data_service.messaging import MessageProcessor


def validate_date_format(_ctx, _param, value):
    """Validate user input datetime"""
    if re.match(DATETIME_REGEX, value):
        return value
    raise click.BadParameter("Wrong date format")


def datetime_range(start: datetime, end: datetime, delta: timedelta) -> Generator[datetime, None, None]:
    """Returns datetime range"""
    current = start
    while current < end:
        yield current
        current += delta


def get_energy_values(smart_meter_id: int, measurements_date: str) -> List:
    """Returns list of smart meter data.
    :param smart_meter_id: Smart meter ID.
    :param measurements_date: Date that the user desires to generate energy values for. Format:'%Y-%m-%d'.
    :return: return list of json with smart data: energy_kwh, timestamp, smart_meter_id
    :rtype: list
    :Example:
    Return:
    [{"energy_kwh": 2.6,
    "timestamp": "2021-05-12 00:00:00",
    "smart_meter_id": 1}]
    """
    energy_values = []
    try:
        start = datetime.strptime(measurements_date, "%Y-%m-%d")
    except ValueError as error:
        raise click.BadParameter(f"Wrong date. {error}")

    delta = timedelta(minutes=TIME_INTERVALS_MINUTES)
    end = start + timedelta(days=READING_DURATION_DAYS) + delta

    for time_stamp in datetime_range(start=start, end=end, delta=delta):
        energy_kwh = round(uniform(0, 10), 1)
        smart_data = {
            "energy_kwh": energy_kwh,
            "timestamp": str(time_stamp),
            "smart_meter_id": smart_meter_id,
        }
        energy_values.append(json.dumps(smart_data))
    return energy_values


@click.command()
@click.option("--smart_meter_id", prompt="Smart meter ID", type=int, help="Smart meter ID.")
@click.option(
    "--measurements_date",
    prompt="Measurements date in format: %Y-%m-%d",
    callback=validate_date_format,
    type=str,
    help="Date that the user desires to generate energy values for. Format should be: %Y-%m-%d, eg. 2021-05-12",
)
def publish_smart_data_in_intervals(smart_meter_id: int, measurements_date: str) -> None:
    """Publish energy values to the broker.
    :param smart_meter_id: Smart meter ID.
    :param measurements_date: Date that the user desires to generate energy values for. Format:'%Y-%m-%d'.
    :Example:
    Published data:
    {"energy_kwh": <random value between 0-1>,
    "timestamp": <time that the energy was measured>,
    "smart_meter_id": <id of the smart meter>}
    """
    time_intervals_seconds = TIME_INTERVALS_MINUTES * 60
    click.echo(f"Start publishing data for smart meter {smart_meter_id} on {measurements_date}")
    with MessageProcessor() as processor:
        energy_values = get_energy_values(smart_meter_id, measurements_date)
        for index, smart_data in enumerate(energy_values, 1 - len(energy_values)):
            processor.publish(smart_data)
            click.echo(f"Publishing data: {smart_data}")
            if index:
                time.sleep(time_intervals_seconds)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    publish_smart_data_in_intervals()
