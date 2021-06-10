from datetime import datetime
from typing import List

from sqlalchemy import and_, create_engine, engine
from sqlalchemy.orm import Session, sessionmaker

from src.smart_data_service.config import DB_URL
from src.smart_data_service.models import SmartDataDB
from src.smart_data_service.schemas import SmartData


class DbSession:
    """
    Postgresql connector
    """

    def __init__(self):
        self._url: str = DB_URL
        self.engine: engine.Engine
        self.db_session: Session
        # self.engine: Optional[engine.Engine] = None
        # self.db_session: Optional[Session] = None

    def create_session(self, echo=False):
        """Create database session"""
        self.engine = create_engine(self._url, echo=echo)
        db_session_maker = sessionmaker(bind=self.engine, autocommit=False)
        self.db_session = db_session_maker()

    def __enter__(self):
        self.create_session()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db_session.close()

    def add_smart_data(self, smart_data: SmartData) -> None:
        """Add smart_data to the database."""
        try:
            new_asset = SmartDataDB(
                smart_meter_id=smart_data.smart_meter_id,
                time_stamp=smart_data.time_stamp,
                energy_kwh=smart_data.energy_kwh,
            )
            self.db_session.add(new_asset)
            self.db_session.commit()
        except Exception as exc:
            self.db_session.rollback()
            raise exc

    def query_smart_data_w_time_range(
        self,
        smart_meter_id: int,
        the_daterange_lower: datetime,
        the_daterange_upper: datetime,
    ) -> List[SmartDataDB]:
        """Query the database for a specific smart meter in a provided date range."""
        results = (
            self.db_session.query(SmartDataDB)
            .filter(
                and_(
                    SmartDataDB.smart_meter_id == smart_meter_id,
                    SmartDataDB.time_stamp >= the_daterange_lower,
                    SmartDataDB.time_stamp <= the_daterange_upper,
                )
            )
            .all()
        )
        return results
