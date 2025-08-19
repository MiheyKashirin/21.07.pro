from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, REAL, Enum
from financial_tracker.dataBase import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    password = Column(String(50))
    email = Column(String(120), unique=True)
    birth_date = Column(DateTime)
    country = Column(String(50), nullable=True)



    def __repr__(self):
        return f'<User {self.name!r}>'


class  Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    owner = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))


class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Primary Key
    description = Column(String(100))
    category = Column(Integer, ForeignKey('category.id', ondelete='CASCADE'))
    owner = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    type = Column(Enum('income', 'spend'))
    date = Column(DateTime)
    amount = Column(REAL)