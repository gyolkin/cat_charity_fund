from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class CharityDonationParent(Base):
    """
    Родительский класс моделей пожертвования и проекта.
    """

    __abstract__ = True

    full_amount: Integer = Column(Integer, default=0)
    invested_amount: Integer = Column(Integer, default=0)
    fully_invested: Boolean = Column(Boolean, default=False)
    create_date: DateTime = Column(DateTime, default=datetime.now)
    close_date: DateTime = Column(DateTime)

    def make_fully_invested(self):
        """Закрывает проект или пожертвование."""
        self.fully_invested = True
        self.close_date = datetime.now()
