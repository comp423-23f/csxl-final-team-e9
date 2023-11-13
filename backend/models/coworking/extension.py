from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from backend.models.coworking.reservation import Reservation


class ExtensionState(str, Enum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


class ExtensionRequest(Reservation, BaseModel):
    state: ExtensionState
    current: Reservation | None = None
    newEnd: datetime | None = None
