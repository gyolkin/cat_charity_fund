from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.crud import charity_project_crud, donation_crud
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.models import User
from app.schemas.donation import AllDonationDB, DonationCreate, UserDonationDB
from app.services import investing_worker

router = APIRouter()


@router.get(
    "/",
    response_model=List[AllDonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Получает список всех пожертвований.
    """
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    "/my",
    response_model=List[UserDonationDB],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получить список моих пожертвований."""
    user_donations = await donation_crud.get_multi_by_user_id(user.id, session)
    return user_donations


@router.post(
    "/",
    response_model=UserDonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
    donation_input: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(donation_input, session, user)
    session.add_all(
        investing_worker(
            new_donation, await charity_project_crud.get_multi_opened(session)
        )
    )
    await session.commit()
    await session.refresh(new_donation)
    return new_donation
