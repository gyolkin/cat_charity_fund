from typing import Generic, List, Optional, Type, TypeVar

from fastapi import HTTPException, encoders, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.core.user import User

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Базовый класс Create-Read-Update-Delete действий.
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_or_404(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> ModelType:
        """Получает объект из базы данных или вызывает ошибку 404."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        db_obj = db_obj.scalars().first()
        if db_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Запрашиваемый объект не найден.",
            )
        return db_obj

    async def get_id_by_name(
        self,
        name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        obj_id = await session.execute(
            select(self.model.id).where(self.model.name == name)
        )
        return obj_id.scalars().first()

    async def get_multi(self, session: AsyncSession) -> List[ModelType]:
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def get_multi_opened(self, session: AsyncSession) -> List[ModelType]:
        db_objs = await session.execute(
            select(self.model)
            .where(self.model.fully_invested == 0)
            .order_by(self.model.create_date)
        )
        return db_objs.scalars().all()

    async def get_multi_by_user_id(
        self,
        user_id: int,
        session: AsyncSession,
    ) -> List[ModelType]:
        db_objs = await session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        return db_objs.scalars().all()

    async def create(
        self, obj_in, session: AsyncSession, user: Optional[User] = None
    ) -> ModelType:
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data["user_id"] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ) -> ModelType:
        obj_data = encoders.jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ) -> ModelType:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
