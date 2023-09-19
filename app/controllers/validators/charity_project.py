from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.crud import charity_project_crud


async def check_project_name_not_exists(
    project_name: str,
    session: AsyncSession,
) -> None:
    """
    Проверяет, что проект с таким названием не существует в базе данных.

    Ввод:
        project_name (str): Имя запрашиваемого проекта.
        session (AsyncSession): Текущая сессия.
    Ошибка:
        400
    """
    project_id = await charity_project_crud.get_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )


async def check_project_not_funded(invested_amount: int) -> None:
    """
    Проверяет, что в данный проект не вложены средства.

    Ввод:
        invested_amount (int): Вложенная сумма.
    Ошибка:
        400
    """
    if invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )


async def check_project_amount(invested_amount: int, full_amount: int) -> None:
    """
    Проверяет, что целевая сумма больше или равна уже вложенной.

    Ввод:
        invested_amount (int): Вложенная сумма.
        full_amount (int): Целевая сумма.
    Ошибка:
        400
    """
    if invested_amount > full_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Невозможно установить целевую сумму ниже уже вложенной.",
        )


async def check_project_status(fully_invested: bool) -> None:
    """
    Проверяет, что проект на данный момент не закрыт.

    Ввод:
        fully_invested (bool): Значение True/False,
        указывающее на статус проекта.
    Ошибка:
        400
    """
    if fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!",
        )
