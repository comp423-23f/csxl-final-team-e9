"""Entity for Reservations."""

from datetime import datetime, timedelta
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from ..entity_base import EntityBase
from ...models.coworking import Reservation, ReservationState
from .room_entity import RoomEntity
from .seat_entity import SeatEntity
from ..user_entity import UserEntity
from .reservation_user_table import reservation_user_table
from .reservation_seat_table import reservation_seat_table
from typing import Self

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class ReservationEntity(EntityBase):
    __tablename__ = "coworking__reservation"
    __table_args__ = (
        Index("coworking__reservation_time_idx", "start", "end", "state", unique=False),
    )

    # Reservation Model Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    state: Mapped[ReservationState] = mapped_column(String, nullable=False)
    walkin: Mapped[bool] = mapped_column(Boolean, nullable=False)
    room_id: Mapped[str] = mapped_column(
        String, ForeignKey("coworking__room.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    # Relationships
    users: Mapped[list[UserEntity]] = relationship(secondary=reservation_user_table)
    seats: Mapped[list[SeatEntity]] = relationship(secondary=reservation_seat_table)
    room: Mapped[RoomEntity] = relationship("RoomEntity")

    def to_model(self) -> Reservation:
        """Converts the entity to a model.

        Returns:
            Reservation: The model representation of the entity."""
        return Reservation(
            id=self.id,
            start=self.start,
            end=self.end,
            state=self.state,
            users=[user.to_model() for user in self.users],
            seats=[seat.to_model() for seat in self.seats],
            walkin=self.walkin,
            room=self.room.to_model() if self.room else None,
            created_at=self.created_at,
            updated_at=self.updated_at,
            time_remaining=self.time_remaining,
        )

    @classmethod
    def from_model(cls, model: Reservation, session: Session | None = None) -> Self:
        """Create an ReservationEntity from a Reservation model.

        Args:
            model (Reservation): The model to create the entity from.

        Returns:
            Self: The entity (not yet persisted)."""

        return cls(
            id=model.id,
            start=model.start,
            end=model.end,
            state=model.state,
            walkin=model.walkin,
            room_id=model.room.id if model.room else None,
            users=[session.get(UserEntity, user.id) for user in model.users]
            if session
            else [],
            seats=[session.get(SeatEntity, seat.id) for seat in model.seats]
            if session
            else [],
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    def is_eligible_for_extension(self) -> bool:
        """Determines if the reservation is eligible for an extension.

        This method checks whether the reservation can be extended based on the remaining time until its scheduled end.
        A reservation is eligible for an extension if there are 30 minutes or less remaining.

        Returns:
            bool: True if the reservation is eligible for an extension
            (less than or equal to 30 minutes remaining until the end), otherwise False.
        """
        return self.time_remaining <= 30 * 60 
    
    @property
    def time_remaining(self) -> int:
        """Calculates the time remaining for the reservation in seconds."""
        now = datetime.now()
        remaining = self.end - now
        return remaining <= timedelta(minutes=30)
