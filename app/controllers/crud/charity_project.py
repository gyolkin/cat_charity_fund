from app.controllers.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)


class CRUDCharityProject(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]
):
    pass


crud = CRUDCharityProject(CharityProject)
