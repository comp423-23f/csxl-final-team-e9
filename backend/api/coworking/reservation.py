"""Coworking Client Reservation API

This API is used to make and manage reservations."""

from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta
from ..authentication import registered_user
from ...services.coworking.reservation import ReservationService
from ...models import User
from ...models.coworking import (
    Reservation,
    ReservationRequest,
    ReservationPartial,
    ReservationState,
)
from backend.models.coworking.extension import ExtensionRequest

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


api = APIRouter(prefix="/api/coworking")
openapi_tags = {
    "name": "Coworking",
    "description": "Coworking reservations, status, and XL Ambassador functionality.",
}


@api.post("/reservation", tags=["Coworking"])
def draft_reservation(
    reservation_request: ReservationRequest,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation:
    """Draft a reservation request."""
    return reservation_svc.draft_reservation(subject, reservation_request)


@api.get("/reservation/{id}", tags=["Coworking"])
def get_reservation(
    id: int,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation:
    return reservation_svc.get_reservation(subject, id)


@api.get("/reservation/{id}/time-remaining", tags=["Coworking"])
def get_time_remaining(
    id: int,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> int:
    return reservation_svc.get_reservation_time_remaining(id)


@api.get("/reservation/{id}/max-extension", tags=["Coworking"])
def get_max_extension_amount(
    id: int,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> int:
    return reservation_svc.max_extension_amount(id)


@api.put("/reservation/{id}", tags=["Coworking"])
def update_reservation(
    reservation: ReservationPartial,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation:
    """Modify a reservation."""
    return reservation_svc.change_reservation(subject, reservation)


@api.delete("/reservation/{id}", tags=["Coworking"])
def cancel_reservation(
    id: int,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation:
    """Cancel a reservation."""
    return reservation_svc.change_reservation(
        subject, ReservationPartial(id=id, state=ReservationState.CANCELLED)
    )


@api.put("/reservation/{id}/extend", tags=["Coworking"])
def extend_reservation(
    extension_request: ExtensionRequest,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation:
    """Extend a reservation's end time.
    This endpoint allows a user to extend their current reservation by up to an additional hour,
    provided there is less than 30 minutes remaining in their current reservation.

    Args:
        extension_request (ExtensionRequest): includes the id of the reservation to extend and the duration by which to extend the reservation, 
        up to a maximum of one hour.
        subject (User): The user requesting the reservation extension.

    Returns:
        Reservation: The updated reservation with the new end time."""
    return reservation_svc.extend_reservation(extension_request.id, extension_request.extension_duration)