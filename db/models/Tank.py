from db.models.BaseModelClass import BaseModelClass
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Tank(BaseModelClass):
    __tablename__ = "tank"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    mqtt_name = Column(String(64), nullable=False)
    logs = relationship("ProcessLog", back_populates="tank")
    actuators = relationship("Actuator", back_populates="tank")
    sensors = relationship("Sensor", back_populates="tank")