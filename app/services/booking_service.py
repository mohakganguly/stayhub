from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.schemas import BookingCreate
from app.exceptions import (
    AuthorizationError,
    ConflictError,
    NotFoundError,
    ValidationError,
)


def create_booking(
    db: Session,
    booking_data: BookingCreate,
    user_id: int,
) -> models.Booking:

    # 1. Find and lock the property
    property_obj = db.execute(
        select(models.Property)
        .where(
            models.Property.id == booking_data.property_id
        )
        .with_for_update()
    ).scalar_one_or_none()

    if property_obj is None:
        raise NotFoundError(
            "Property not found"
        )

    # 2. Validate number of guests
    if booking_data.guests > property_obj.max_guests:
        raise ValidationError(
            f"Property allows a maximum of "
            f"{property_obj.max_guests} guests"
        )

    # 3. Check for overlapping bookings
    overlap_statement = select(models.Booking).where(
        models.Booking.property_id
        == booking_data.property_id,

        models.Booking.status.in_(
            ["PENDING", "CONFIRMED"]
        ),

        models.Booking.check_in
        < booking_data.check_out,

        models.Booking.check_out
        > booking_data.check_in,
    )

    overlapping_booking = db.execute(
        overlap_statement
    ).scalar_one_or_none()

    if overlapping_booking is not None:
        raise ConflictError(
            "Property is already booked for "
            "the selected dates"
        )

    # 4. Calculate number of nights
    number_of_nights = (
        booking_data.check_out
        - booking_data.check_in
    ).days

    # 5. Calculate total price
    total_price = (
        number_of_nights
        * property_obj.price_per_night
    )

    # 6. Create booking
    booking = models.Booking(
        property_id=booking_data.property_id,
        user_id=user_id,
        check_in=booking_data.check_in,
        check_out=booking_data.check_out,
        guests=booking_data.guests,
        total_price=total_price,
        status="PENDING",
    )

    db.add(booking)

    # 7. Commit transaction
    try:
        db.commit()
        db.refresh(booking)
        return booking

    except Exception:
        db.rollback()
        raise


def get_booking(
    db: Session,
    booking_id: int,
) -> models.Booking:

    statement = select(models.Booking).where(
        models.Booking.id == booking_id
    )

    booking = db.execute(
        statement
    ).scalar_one_or_none()

    if booking is None:
        raise NotFoundError(
            "Booking not found"
        )

    return booking


def get_property_bookings(
    db: Session,
    property_id: int,
) -> list[models.Booking]:

    statement = (
        select(models.Booking)
        .where(
            models.Booking.property_id == property_id
        )
        .order_by(
            models.Booking.check_in.asc()
        )
    )

    return (
        db.execute(statement)
        .scalars()
        .all()
    )


def get_user_bookings(
    db: Session,
    user_id: int,
) -> list[models.Booking]:

    statement = (
        select(models.Booking)
        .where(
            models.Booking.user_id == user_id
        )
        .order_by(
            models.Booking.created_at.desc()
        )
    )

    return (
        db.execute(statement)
        .scalars()
        .all()
    )


def cancel_booking(
    db: Session,
    booking_id: int,
    user_id: int,
) -> models.Booking:

    booking = get_booking(
        db=db,
        booking_id=booking_id,
    )

    # Authorization
    if booking.user_id != user_id:
        raise AuthorizationError(
            "You are not allowed to modify this booking"
        )

    # State validation
    if booking.status == "CANCELLED":
        raise ConflictError(
            "Booking is already cancelled"
        )

    if booking.status != "PENDING":
        raise ConflictError(
            "Only pending bookings can be cancelled"
        )

    try:
        booking.status = "CANCELLED"

        db.commit()
        db.refresh(booking)

        return booking

    except Exception:
        db.rollback()
        raise