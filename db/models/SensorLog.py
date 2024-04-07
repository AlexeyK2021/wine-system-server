from db.models.BaseModelClass import BaseModelClass
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from db.models.Sensor import Sensor


class SensorLog(BaseModelClass):
    __tablename__ = "sensor_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False)
    value = Column(Float, nullable=False)
    sensor_id = Column(Integer, ForeignKey("sensor.id"))
    sensor = relationship("Sensor", back_populates="logs")
