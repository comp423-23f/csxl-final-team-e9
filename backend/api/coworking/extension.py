"""This API is used to establish a route for the extension.py."""

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

api = APIRouter(prefix="/api/coworking")
openapi_tags = {
    "name": "Coworking",
    "description": "Coworking reservations, status, and XL Ambassador functionality.",
}

@api.put("/reservation/{id}", tags=["Coworking"])
def update_extension_request(
    extension_request: ExtensionRequest,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation: # type: ignore