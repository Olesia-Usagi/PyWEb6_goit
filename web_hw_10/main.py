from models import Record, Contact, EmailContact, PhoneContact, AddressContact

rec = Record(first_name='Пітер', last_name='Гаррісон').save()

rec1 = EmailContact(contact=rec)
rec1.email = 'asd@gmail.com'
rec1.save()
