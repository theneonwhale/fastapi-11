from sqlalchemy import Column, Integer, String, DateTime, func, Date
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    surname = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    birthday = Column(Date, default=None)
    additional_info = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(name='{self.name}', surname='{self.surname}', email='{self.email}', phone='{self.phone}')>"
