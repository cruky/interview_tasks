import json
import re
from datetime import datetime, timedelta

import pytest

import smart_data_publisher

# pylint: disable = "W0621"

def pytest_configure():
    """Set global variables"""
    pytest.READING_DURATION_DAYS = 1
    pytest.TIME_INTERVALS_MINUTES = 15


@pytest.fixture()
def time_range_setup():
    """Set a day range, from midnight to midnight"""
    start = datetime.strptime("2021-01-01", "%Y-%m-%d")
    delta = timedelta(minutes=15)
    end = start + timedelta(days=1) + delta
    return start, end, delta


@pytest.fixture()
def datetime_range_list(time_range_setup):
    """get list of datetime range"""
    start, end, delta = time_range_setup
    datetime_range_gen = smart_data_publisher.datetime_range(start=start, end=end, delta=delta)
    return list(datetime_range_gen)


@pytest.fixture()
def get_energy_values():
    """Set a day range, from midnight to midnight"""
    energy_values = smart_data_publisher.get_energy_values(1, "2021-01-01")
    return energy_values


@pytest.fixture()
def get_first_element_as_dict(get_energy_values):
    """Get first element from energy values as dict"""
    return json.loads(get_energy_values[0])


@pytest.fixture()
def get_last_element_as_dict(get_energy_values):
    """Get last element from energy values as dict"""
    return json.loads(get_energy_values[-1])


def test_energy_keys(get_first_element_as_dict):
    """Check keys in elements"""
    assert ["energy_kwh", "timestamp", "smart_meter_id"] == list(get_first_element_as_dict.keys())


def test_energy_types(get_first_element_as_dict):
    """Check keys in elements"""
    time_stamp_regex = r"^\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2}$"
    is_energy_kwh_float = isinstance(get_first_element_as_dict.get("energy_kwh"), float)
    is_smart_meter_id_int = isinstance(get_first_element_as_dict.get("smart_meter_id"), int)
    is_timestamp_datetime = isinstance(get_first_element_as_dict.get("timestamp"), str) and re.match(
        time_stamp_regex, get_first_element_as_dict.get("timestamp")
    )

    assert all([is_energy_kwh_float, is_smart_meter_id_int, is_timestamp_datetime])


def test_energy_values_len(get_energy_values):
    """Check number of energy values in the list
    4 x 24=96
    """
    assert len(get_energy_values) == 97


def test_first_energy_value(get_first_element_as_dict):
    """Check first energy value"""
    timestamp = get_first_element_as_dict.get("timestamp")
    smart_meter_id = get_first_element_as_dict.get("smart_meter_id")
    assert timestamp == "2021-01-01 00:00:00" and smart_meter_id == 1


def test_last_energy_value(get_last_element_as_dict):
    """Check last energy value"""
    timestamp = get_last_element_as_dict.get("timestamp")
    smart_meter_id = get_last_element_as_dict.get("smart_meter_id")
    assert timestamp == "2021-01-02 00:00:00" and smart_meter_id == 1


def test_datetime_range_len(datetime_range_list):
    """Check number of datetime in the list
    4 x 24=96
    """
    assert len(datetime_range_list) == 97


def test_first_datetime_is_midnight(datetime_range_list):
    """Check if first datetime is at midnight"""
    first, *_ = datetime_range_list
    assert datetime(2021, 1, 1, 0, 0) == first


def test_last_datetime_is_midnight(datetime_range_list):
    """Check if last datetime is at midnight"""
    *_, last = datetime_range_list
    assert datetime(2021, 1, 2, 0, 0) == last
