from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.crud import charity_project_crud, donation_crud
from app.models import CharityProject, Donation

ModelType = TypeVar("ModelType", CharityProject, Donation)


async def investing_worker(obj: ModelType, session: AsyncSession) -> ModelType:
    """
    Функция, выполняющая инвестирование неиспользованных средств в проекты.

    Описание: Пожертвование распределяется между проектами по принципу FIFO.
        Если проекты закрыты, то пожертвование используется в новом проекте.

    Input:
        obj (Donation | CharityProject): Объект нового пожертвования
            или проекта.
        session (AsyncSession): Асинхронная сессия.
    Output:
        obj (Donation | CharityProject): Объект преобразованного пожертвования
            или проекта.

    Функция рекурсивно работает до тех пор, пока не останутся только
        закрытые проекты или пожертвования.
    """
    open_project = await charity_project_crud.get_first_opened(session)
    open_donation = await donation_crud.get_first_opened(session)

    if not open_project or not open_donation:
        return obj

    project_to_close = open_project.full_amount - open_project.invested_amount
    donation_to_close = (
        open_donation.full_amount - open_donation.invested_amount
    )
    distributable_amount = min(project_to_close, donation_to_close)
    open_project.invested_amount += distributable_amount
    open_donation.invested_amount += distributable_amount

    if open_project.invested_amount == open_project.full_amount:
        open_project.make_fully_invested()
    if open_donation.invested_amount == open_donation.full_amount:
        open_donation.make_fully_invested()

    session.add(open_project)
    session.add(open_donation)
    await session.commit()
    await session.refresh(open_project)
    await session.refresh(open_donation)
    await investing_worker(obj, session)
    return obj
