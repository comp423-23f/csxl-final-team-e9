"""This API is used to extend reservations."""

from fastapi import APIRouter, Depends, HTTPException

from backend.models.coworking.extension import ExtensionRequest
from ..authentication import registered_user
from ...services.coworking.reservation import ReservationService
from ...models import User
from ...models.coworking import (
    Reservation,
    ReservationRequest,
    ReservationPartial,
    ReservationState,
)

__authors__ = ["Isha Atre, Chloe Carroll, Lauren Jones, Soumya Mahavadi"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

api = APIRouter(prefix="/api/coworking")
openapi_tags = {
    "name": "Coworking",
    "description": "Extending coworking reservations.",
}

@api.put("/reservation/{id}", tags=["Coworking"])
def extend_reservation(
    extensionRequest: ExtensionRequest,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation: # type: ignore