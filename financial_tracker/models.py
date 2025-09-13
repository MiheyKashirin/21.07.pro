from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, REAL
from dataBase import Base

class User(Base):
    __tablename__ = 'user'  # название таблицы user, чтобы совпадало с ForeignKey
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    password = Column(String(50))
    email = Column(String(120), unique=True)
    birth_date = Column(DateTime, nullable=True)  # можно оставить nullable=True
    country = Column(String(50), nullable=True)

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    owner = Column(Integer, ForeignKey('user.id'))

class Transactions(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    description = Column(String(200))
    category = Column(Integer, ForeignKey('category.id'))
    amount = Column(REAL, nullable=False)
    datetime = Column(DateTime, nullable=False)
    owner = Column(Integer, ForeignKey('user.id'))
    type = Column(String(10))
