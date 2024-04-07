from db.models.BaseModelClass import BaseModelClass
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class ParameterType(BaseModelClass):
    __tablename__ = "param_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    description = Column(String(256), nullable=True)
    params = relationship("Parameter", back_populates="type")
