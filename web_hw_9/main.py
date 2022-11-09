from sqlalchemy.orm import joinedload

from models import session, Contact, Address, Email, Phone


def get_all_names():
    contacts = session.query(Contact).options(joinedload("cont_address")).all()
    for contact in contacts:
        print(vars(contact))
        print(f'{[f" address is {n.address_ad}" for n in contact.cont_address]}')


if __name__ == '__main__':
    get_all_names()
