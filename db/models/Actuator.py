from db.models.BaseModelClass import BaseModelClass
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.models.Tank import Tank
from db.models.ActuatorType import ActuatorType


class Actuator(BaseModelClass):
    __tablename__ = "actuator"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    model = Column(String(128), nullable=True)
    mqtt_name = Column(String(64), nullable=False)
    type_id = Column(Integer, ForeignKey("actuator_type.id"))
    type = relationship("ActuatorType", back_populates="actuators")
    tank_id = Column(Integer, ForeignKey("tank.id"))
    tank = relationship("Tank", back_populates="actuators")
    logs = relationship("ActuatorLog", back_populates="actuator")

