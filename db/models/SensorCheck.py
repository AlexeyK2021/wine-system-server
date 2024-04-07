from db.models.BaseModelClass import BaseModelClass
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from db.models.Sensor import Sensor


class SensorCheck(BaseModelClass):
    __tablename__ = "sensor_check"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    sensor_id = Column(Integer, ForeignKey("sensor.id"))
    sensor = relationship("Sensor", back_populates="checks")
