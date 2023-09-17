from typing import Any, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.crud.base import CRUDBase
from app.models import Donation
from app.schemas.donation import DonationCreate


class CRUDDonation(CRUDBase[Donation, DonationCreate, Any]):
    async def get_multi_by_user_id(
        self,
        user_id: int,
        session: AsyncSession,
    ) -> List[Donation]:
        db_objs = await session.execute(
            select(Donation).where(Donation.user_id == user_id)
        )
        db_objs = db_objs.scalars().all()
        return db_objs


crud = CRUDDonation(Donation)
