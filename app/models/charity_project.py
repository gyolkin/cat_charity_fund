from sqlalchemy import Column, String, Text

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

    name: String = Column(String(100), unique=True, nullable=False)
    description: Text = Column(Text, nullable=False)
