from db.models.BaseModelClass import BaseModelClass
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class SensorType(BaseModelClass):
    __tablename__ = "sensor_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    description = Column(String(256), nullable=True)
    sensors = relationship("Sensor", back_populates="type")
