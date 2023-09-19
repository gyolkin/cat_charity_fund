from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class CharityDonationParent(Base):
    """
    Родительский класс моделей пожертвования и проекта.
    """

    __abstract__ = True

    full_amount = Column(
        Integer, CheckConstraint("full_amount >= 0"), default=0
    )
    invested_amount = Column(
        Integer, CheckConstraint("full_amount >= invested_amount"), default=0
    )
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def make_fully_invested(self):
        """Закрывает проект или пожертвование."""
        self.fully_invested = True
        self.close_date = datetime.now()
