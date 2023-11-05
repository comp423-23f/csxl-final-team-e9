from datetime import datetime
from pydantic import BaseModel
from backend.models.coworking.reservation import Reservation


class ExtensionRequest(Reservation, BaseModel):
    current: Reservation | None = None
    newEnd: datetime | None = None
