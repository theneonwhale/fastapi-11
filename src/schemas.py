from datetime import date, datetime

from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    surname: str = Field(min_length=3, max_length=50)
    email: EmailStr
    phone: str = Field(min_length=10, max_length=16)
    birthday: date = None
    additional_info: str = Field(max_length=100)


class ContactResponse(BaseModel):
    id: int = 1
    name: str
    surname: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
