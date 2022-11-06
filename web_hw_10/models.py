from mongoengine import *
from mongoengine.fields import StringField

connect(host='mongodb://localhost:27017/HW10')


class Record(Document):
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)


class Contact(Document):
    contact = ReferenceField(Record, reverse_delete_rule=CASCADE)
    meta = {'allow_inheritance': True}


class PhoneContact(Contact):
    phone = StringField()


class EmailContact(Contact):
    email = StringField()


class AddressContact(Contact):
    address = StringField()
