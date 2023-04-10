from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session
from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(limit: int, offset: int, db: Session):
    contacts = db.query(Contact).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def get_contact_by_email(email: str, db: Session):
    contact = db.query(Contact).filter_by(email=email).first()
    return contact


async def get_contact_by_phone(phone: str, db: Session):
    contact = db.query(Contact).filter_by(phone=phone).first()
    return contact


async def create_contact(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.additional_info = body.additional_info
        db.commit()
    return contact


async def delete_contact(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(query: str, db: Session):
    contacts = db.query(Contact).filter(
        func.lower(Contact.name).contains(func.lower(query)) |
        func.lower(Contact.surname).contains(func.lower(query)) |
        func.lower(Contact.email).contains(func.lower(query)) |
        func.lower(Contact.phone).contains(func.lower(query))
    ).all()
    return contacts


async def get_birthdays(db: Session):
    now = datetime.now().date()
    contacts = db.query(Contact).all()
    birthday_contacts = []
    for contact in contacts:
        birthday = contact.birthday
        if birthday:
            birthday_this_year = birthday.replace(year=now.year)
            days_until_birthday = (birthday_this_year - now).days
            if days_until_birthday in range(8):
                birthday_contacts.append(contact)

    return birthday_contacts
