from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.crud import charity_project_crud
from app.controllers.validators.charity_project import (
    check_project_amount,
    check_project_name_not_exists,
    check_project_not_funded,
    check_project_status,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services import investing_worker

router = APIRouter()


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    project_input: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Создаёт благотворительный проект.
    """
    await check_project_name_not_exists(project_input.name, session)
    new_project = await charity_project_crud.create(project_input, session)
    new_project = await investing_worker(new_project, session)
    return new_project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Удаляет проект. Нельзя удалить проект, в который уже были
    инвестированы средства, его можно только закрыть.
    """
    project = await charity_project_crud.get_or_404(project_id, session)
    await check_project_not_funded(project.invested_amount)
    deleted_project = await charity_project_crud.remove(project, session)
    return deleted_project


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    project_input: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной.
    """
    project = await charity_project_crud.get_or_404(project_id, session)
    if project_input.full_amount:
        await check_project_amount(
            project.invested_amount, project_input.full_amount
        )
    if project_input.name:
        await check_project_name_not_exists(project_input.name, session)
    await check_project_status(project.fully_invested)
    project = await charity_project_crud.update(
        project, project_input, session
    )
    return project
