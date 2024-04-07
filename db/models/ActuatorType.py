from db.models.BaseModelClass import BaseModelClass
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class ActuatorType(BaseModelClass):
    __tablename__ = "actuator_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    description = Column(String(256), nullable=True)
    actuators = relationship("Actuator", back_populates="type")
