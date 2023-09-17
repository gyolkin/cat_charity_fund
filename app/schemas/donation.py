from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: Optional[PositiveInt]


class DonationCreate(DonationBase):
    full_amount: PositiveInt


# class CharityProjectUpdate(CharityProjectBase):
#     pass

#     @validator("name")
#     def name_cannot_be_null(cls, value):
#         if value is None:
#             raise ValueError("Название проекта не может быть пустым.")
#         return value


# class CharityProjectDB(CharityProjectCreate):
#     id: int
#     invested_amount: int
#     fully_invested: bool
#     create_date: datetime
#     close_date: Optional[datetime]

#     class Config:
#         orm_mode = True
