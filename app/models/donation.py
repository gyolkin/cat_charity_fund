from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import CharityDonationParent


class Donation(CharityDonationParent):
    """
    Модель проекта пожертвований.

    Атрибуты:
        id (int): Уникальный id.
        user_id (int): Ссылка на пользователя, сделавшего пожертвование.
        comment (str): Комментарий к пожертвованию.
        full_amount (int): Сумма пожертвования.
        invested_amount (int): Сумма, которая распределена по проектам.
        fully_invested (bool): Указывает, все ли деньги из пожертвования
            были переведены в тот или иной проект.
        create_date (datetime): Дата внесения пожертвования.
        close_date (datetime): Дата, когда сумма была распределена по проектам.
    """

    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text)
