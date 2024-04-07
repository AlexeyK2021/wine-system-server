from db.models.BaseModelClass import BaseModelClass
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db.models.ResultCode import ResultCode
from db.models.Tank import Tank


class ProcessLog(BaseModelClass):
    __tablename__ = "process_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=True)
    tank_id = Column(Integer, ForeignKey("tank.id"))
    tank = relationship("Tank", back_populates="logs")
    result_id = Column(Integer, ForeignKey("result_code.id"))
    result = relationship("ResultCode", back_populates="logs")
