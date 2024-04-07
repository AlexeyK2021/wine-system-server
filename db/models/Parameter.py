from db.models.BaseModelClass import BaseModelClass
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from db.models.ParameterType import ParameterType

class Parameter(BaseModelClass):
    __tablename__ = "parameter"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    min_value = Column(Float, nullable=False)
    max_value = Column(Float, nullable=False)
    type_id = Column(Integer, ForeignKey("param_type"))
    type = relationship("ParameterType", back_populates="params")
    sensors = relationship("Sensor", back_populates="parameter")
