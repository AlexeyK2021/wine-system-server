from db.models.BaseModelClass import BaseModelClass
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class ResultCode(BaseModelClass):
    __tablename__ = "result_code"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    description = Column(String(256), nullable=True)
    logs = relationship("ProcessLog", back_populates="result")
