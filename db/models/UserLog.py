from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db.models.BaseModelClass import BaseModelClass
from db.models.User import User
from db.models.UserAction import UserAction


class UserLog(BaseModelClass):
    __tablename__ = "user_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False)
    description = Column(String(256), nullable=True)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="user_logs")
    # user = relationship("User")
    action_id = Column(Integer, ForeignKey("user_action.id"))
    # action = relationship("UserAction")
    action = relationship("UserAction", back_populates="logs")
