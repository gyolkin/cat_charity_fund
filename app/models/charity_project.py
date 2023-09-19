from sqlalchemy import Column, String, Text

from app.core.constants import NAME_MAX_LENGTH
from app.models.base import CharityDonationParent


class CharityProject(CharityDonationParent):
    """
    Модель проекта пожертвований.

    Атрибуты:
        id (int): Уникальный id.
        name (str): Уникальное название проекта.
        description (str): Описание проекта.
        full_amount (int): Целевая сумма, которую собирает проект.
        invested_amount (int): Внесенная сумма.
        fully_invested (bool): Указывает, собрана ли целевая сумма.
        create_date (datetime): Дата создания проекта.
        close_date (datetime): Дата закрытия проекта.
    """

    name = Column(String(NAME_MAX_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)
