from db.models.BaseModelClass import BaseModelClass
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.models.SensorType import SensorType
from db.models.Tank import Tank
from db.models.Parameter import Parameter


class Sensor(BaseModelClass):
    __tablename__ = "sensor"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    model = Column(String(128), nullable=True)
    mqtt_name = Column(String(64), nullable=False)
    type_id = Column(Integer, ForeignKey("sensor_type.id"))
    type = relationship("SensorType", back_populates="sensors")
    tank_id = Column(Integer, ForeignKey("tank.id"))
    tank = relationship("Tank", back_populates="sensors")
    parameter_id = Column(Integer, ForeignKey("parameter.id"))
    parameter = relationship("Parameter", back_populates="sensors")
    checks = relationship("SensorCheck", back_populates="sensor")
    logs = relationship("SensorLog", back_populates="sensor")
