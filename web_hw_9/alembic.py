import random
from faker import Faker
from models import session, Contact, Address, Email, Phone, ContactToPhone

fk = Faker('uk_UA')


def create_phones():
    for _ in range(30):
        phone = Phone(
            phone_num=fk.phone_number()
        )
        session.add(phone)
    session.commit()


def create_address():
    for _ in range(15):
        address = Address(
            address_ad=fk.address(),
            contact_id=random.randint(1, 9)
        )
        session.add(address)
    session.commit()


def create_email():
    for _ in range(25):
        email = Email(
            email_mail=fk.email(),
            contact_id=random.randint(1, 9)
        )
        session.add(email)
    session.commit()


def create_contact():
    for _ in range(7):
        contact = Contact(
            cont_name=fk.name()
        )
        session.add(contact)
    session.commit()


def create_relationship():
    names = session.query(Contact).all()
    addresses = session.query(Address).all()
    phones = session.query(Phone).all()
    emails = session.query(Email).all()

    for name in names:
        address = random.choice(addresses)
        email = random.choice(emails)
        rel = ContactToPhone(name_id=name.name_id, phone_id=random.randint(1, 30), address_id=address.address_id,
                             email_id=email.email_id)
        session.add(rel)
    session.commit()


if __name__ == '__main__':
    # create_contact()
    # create_email()
    # create_phones()
    create_address()
    # create_relationship()
