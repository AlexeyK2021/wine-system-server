from db.models.BaseModelClass import BaseModelClass
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

from db.models.Actuator import Actuator


class ActuatorLog(BaseModelClass):
    __tablename__ = "actuator_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    state = Column(Boolean, nullable=False)
    datetime = Column(DateTime, nullable=False)
    actuator_id = Column(Integer, ForeignKey("actuator.id"))
    actuator = relationship("Actuator", back_populates="logs")
