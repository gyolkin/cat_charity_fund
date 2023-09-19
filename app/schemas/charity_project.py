from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    description: Annotated[str, Field(min_length=1)]
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass

    @validator("name", "description")
    def strings_cannot_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Строковые поля не могут быть пустыми.")
        return value.strip()

    @validator("full_amount")
    def full_amount_cannot_be_null(cls, value: int) -> int:
        if value is None or not isinstance(value, int):
            raise ValueError("Целевая сумма проекта не может быть пустой.")
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
