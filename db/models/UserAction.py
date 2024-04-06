from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.models.BaseModelClass import BaseModelClass


class UserAction(BaseModelClass):
    __tablename__ = "user_action"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    description = Column(String(256), nullable=True)
    logs = relationship("UserLog", back_populates="action")
