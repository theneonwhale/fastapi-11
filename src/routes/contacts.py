from typing import List, Optional

from fastapi import Query, Depends, HTTPException, Path, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from src.database.db import get_db
from src.schemas import ContactResponse, ContactModel
from src.repository import contacts as repository_contacts


router = APIRouter(prefix="/contacts", tags=['contacts'])


@router.get('/', response_model=List[ContactResponse], name="get contacts")
async def get_contacts(limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db)):
    print('get_contacts', 12)
    contacts = await repository_contacts.get_contacts(limit, offset, db)
    return contacts


@router.get('/search', response_model=List[ContactResponse])
async def search_contacts(query: Optional[str] = None, db: Session = Depends(get_db)):
    contacts = await repository_contacts.search_contacts(query, db)
    return contacts


@router.get('/birthdays', response_model=List[ContactResponse])
async def get_birthdays(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_birthdays(db)
    return contacts


@router.get('/{contact_id}', response_model=ContactResponse, name="get contact")
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.post('/', response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    has_contact_by_email = await repository_contacts.get_contact_by_email(body.email, db)
    has_contact_by_phone = await repository_contacts.get_contact_by_phone(body.phone, db)
    if has_contact_by_email or has_contact_by_phone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already exists")
    contact = await repository_contacts.create_contact(body, db)
    return contact


@router.put('/{contact_id}', response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    contact.name = body.name
    contact.surname = body.surname
    contact.email = body.email
    contact.phone = body.phone
    contact.birthday = body.birthday
    contact.additional_info = body.additional_info
    db.commit()
    return contact


@router.delete('/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.delete_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    db.delete(contact)
    db.commit()
    return contact
