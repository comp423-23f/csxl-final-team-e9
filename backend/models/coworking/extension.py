from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from backend.models.coworking.reservation import Reservation


class ExtensionRequest(BaseModel):
    id: int
    extension_duration: int
