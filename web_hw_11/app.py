from flask import Flask, render_template, request, redirect
from repo.models import Contact, Phone, Email
from src.connect import db_session
from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

app = Flask(__name__)
app.debug = True
app.env = "development"


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    contacts = db_session.query(Contact).all()
    return render_template("index.html", contacts=contacts, title="Personal Assistant")


@app.route("/detail/<id>", methods=["GET"], strict_slashes=False)
def detail(id):
    contact = db_session.query(Contact).filter(Contact.id == id).first()
    if not contact:
        return render_template("404.html")
    emails = db_session.query(Email).filter(Email.contact == contact).all()
    phones = db_session.query(Phone).filter(Phone.contact == contact).all()
    return render_template("detail.html", contact=contact, emails=emails, phones=phones, title="Contact information")


@app.route("/contact/", methods=["GET", "POST"], strict_slashes=False)
def add_contact():
    if request.method == "POST":
        name = request.form.get("name")
        contact = Contact(name=name)
        db_session.add(contact)
        db_session.commit()
        return redirect("/")
    return render_template("contact.html", title="Add contact")


@app.route("/phone/<id>", methods=["GET", "POST"], strict_slashes=False)
def add_phone(id):
    contact = db_session.query(Contact).filter(Contact.id == id).first()
    if not contact:
        return render_template("404.html", title="404 NOT FOUND")
    if request.method == "POST":
        phone = Phone(phone_number=request.form.get("phone"), contact=contact)
        db_session.add(phone)
        db_session.commit()
        return redirect("/")

    return render_template("phone.html", contact=contact, title="Add phone number")


@app.route("/email/<id>", methods=["GET", "POST"], strict_slashes=False)
def add_email(id):
    contact = db_session.query(Contact).filter(Contact.id == id).first()
    if not contact:
        return render_template("404.html")
    if request.method == "POST":
        email = Email(email=request.form.get("email"), contact=contact)
        db_session.add(email)
        db_session.commit()
        return redirect("/")

    return render_template("email.html", contact=contact, title="Add email")


@app.route("/index/<id>", strict_slashes=False)
def delete(id):
    db_session.query(Contact).filter(Contact.id == id).delete()
    db_session.commit()

    return redirect("/")


@app.route("/contact/<contact_id>/phone_delete/<id>", methods=["GET"], strict_slashes=False)
def delete_phone(contact_id, id):
    contact = db_session.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        return render_template("404.html")
    db_session.query(Phone).filter(contact == contact, Phone.id == id).delete()
    db_session.commit()
    return redirect(f"/detail/{contact_id}")


@app.route("/contact/<contact_id>/email_delete/<id>", methods=["GET"], strict_slashes=False)
def delete_email(contact_id, id):
    contact = db_session.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        return render_template("404.html")
    db_session.query(Email).filter(contact == contact, Email.id == id).delete()
    db_session.commit()
    return redirect(f"/detail/{contact_id}")



if __name__ == "__main__":
    app.run()
