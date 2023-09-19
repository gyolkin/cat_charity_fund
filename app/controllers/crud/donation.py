from typing import Any

from app.controllers.crud.base import CRUDBase
from app.models import Donation
from app.schemas.donation import DonationCreate


class CRUDDonation(CRUDBase[Donation, DonationCreate, Any]):
    pass


crud = CRUDDonation(Donation)
