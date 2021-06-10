from typing import Any, Dict

from sqlalchemy import Column, DateTime, Index, Integer, Numeric, SmallInteger, inspect
from sqlalchemy.ext.declarative import declarative_base

# declarative base class
Base = declarative_base()

# pylint: disable = "R0903"
class SmartDataDB(Base):
    """Mapping for smart_readings table"""

    __tablename__ = "smart_readings"

    id = Column(Integer, nullable=False, primary_key=True)  # pylint: disable = "C0103"
    smart_meter_id = Column(SmallInteger, nullable=False)
    energy_kwh = Column(Numeric(precision=2, scale=1), nullable=False)
    time_stamp = Column(DateTime, index=True, nullable=False)

    __table_args__ = (
        Index(
            "timestamp_idx",
            "time_stamp",
            postgresql_using="btree",
            postgresql_ops={"time_stamp": "DESC"},
        ),
    )

    def __repr__(self):
        return f"smart_meter_id:{self.smart_meter_id} energy_kwh:{self.energy_kwh} time_stamp:{self.time_stamp}"

    def _asdict(self) -> Dict[str, Any]:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
