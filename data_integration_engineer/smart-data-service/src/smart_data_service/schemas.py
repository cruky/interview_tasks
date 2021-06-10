import decimal
import json
from datetime import datetime, timedelta
from re import match
from typing import Type

from pydantic import BaseModel, Json, PositiveInt, root_validator, validator

from src.smart_data_service.config import TIME_STAMP_REGEX


class SmartData(BaseModel):
    """Smart data measurement object"""

    energy_kwh: decimal.Decimal
    time_stamp: datetime
    smart_meter_id: PositiveInt

    @validator("time_stamp", pre=True)
    @classmethod
    def validate_time(cls, value: str) -> str:
        """time that the energy was measured"""
        if isinstance(value, str) and match(TIME_STAMP_REGEX, value):
            return value
        raise ValueError("Invalid format")

    @validator("energy_kwh")
    @classmethod
    def energy_kwh_must_be_float(cls, value: float) -> float:
        """random value between 0-1"""
        pattern = r"^[0-9]{1}\.[0-9]{1}$"
        if match(pattern, str(value)):
            return value
        raise ValueError("must be float")

    @classmethod
    def from_json(cls: Type["SmartData"], input_json: Json) -> "SmartData":
        """Transform json to SmartData object, map fields with field mapping."""
        try:
            data = json.loads(input_json)
            data_field_mapping = {"timestamp": "time_stamp"}
            data = {
                (data_field_mapping[name], val) if name in data_field_mapping else (name, val)
                for name, val in data.items()
            }
            return cls.parse_obj(data)
        except json.JSONDecodeError as exc:
            print(f"ERROR: Invalid JSON: {exc.msg}, line {exc.lineno}, column {exc.colno}")
            return SmartData()

    def __str__(self):
        # pylint: disable = "C0301"
        return f"{{'energy_kwh': {self.energy_kwh}, 'timestamp': {self.time_stamp}, 'smart_meter_id': {self.smart_meter_id}}}"


class SmartDataQuery(BaseModel):
    """Smart data measurement object from query rest api"""

    smart_meter_id: PositiveInt
    start_date: datetime
    end_date: datetime

    @root_validator
    @classmethod
    def check_date_range(cls, values):
        """Check if input data range is less then 1 day"""
        start_date, end_date = values.get("start_date"), values.get("end_date")
        diff = end_date - start_date
        if diff > timedelta(days=1):
            raise ValueError("Date range should be lower than one day")
        return values
