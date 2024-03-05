from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates, DeclarativeBase
import re


class Base(DeclarativeBase):
    pass


class EmailAddress(Base):
    __tablename__ = 'email'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    @validates('email')
    def validate_email(self, key, address):
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(pattern, address):
            raise ValueError('Invalid email address')
        if key != 'email':
            raise ValueError('Key must be "email"')
        return address

    def __repr__(self):
        return f'Email(email={self.email})'
