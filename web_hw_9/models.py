from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
# Реалізуйте зберігання книги контактів з email адресами, телефонами, іменами в базі даних.

Base = declarative_base()
engine = create_engine('sqlite:///HW09.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()


class Contact(Base):
    __tablename__ = 'contacts'
    cont_id = Column(Integer, primary_key=True)
    cont_name = Column(String(60), nullable=False)
    cont_address = relationship("Address", back_populates="contact_ad")
    phones = relationship('Phone', secondary='contacts_to_phone', back_populates='contact')
    cont_email = relationship('Email', back_populates='contact_email')


class Phone(Base):
    __tablename__ = 'phones'
    phone_id = Column(Integer, primary_key=True)
    phone_num = Column(String(60), nullable=False)
    contact = relationship('Contact', secondary='contacts_to_phone', back_populates='phones')


class Address(Base):
    __tablename__ = 'addresses'
    address_id = Column(Integer, primary_key=True)
    address_ad = Column(String(60), nullable=None)
    contact_id = Column('contact_id', ForeignKey('contacts.cont_id', ondelete='CASCADE'), nullable=False)
    contact_ad = relationship("Contact", back_populates="cont_address")


class Email(Base):
    __tablename__ = 'emails'
    email_id = Column(Integer, primary_key=True)
    email_mail = Column(String(60), nullable=False)
    contact_id = Column('contact_id', ForeignKey('contacts.cont_id', ondelete='CASCADE'), nullable=False)
    contact_email = relationship("Contact", back_populates="cont_email")


class ContactToPhone(Base):
    __tablename__ = 'contacts_to_phone'
    id = Column(Integer, primary_key=True)
    contact_id = Column('contact_id', ForeignKey('contacts.cont_id', ondelete='CASCADE'))
    phone_id = Column('phone_id', ForeignKey('phones.phone_id', ondelete='CASCADE'))
