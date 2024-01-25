from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)
    is_deleted = Column(Boolean, default=False)
    account = relationship("Account", back_populates="user")


class Account(Base):
    __tablename__ = 'accounts'
    account_number = Column(Integer, primary_key=True, index=True)
    balance = Column(Integer, default=0)
    is_deleted = Column(Boolean, default=False)
    user = relationship("User", back_populates="account")
    user_id = Column(Integer, ForeignKey("users.id"))
