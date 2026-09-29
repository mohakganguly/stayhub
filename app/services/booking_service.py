from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.schemas import BookingCreate


def create_booking(
    db: Session,
    booking_data: BookingCreate,
) -> models.Booking:

    # 1. Find the property
    property_obj = db.execute(
        select(models.Property).where(
            models.Property.id == booking_data.property_id
        )
        .with_for_update()
    ).scalar_one_or_none()

    if property_obj is None:
        raise ValueError("Property not found")

    # 2. Validate number of guests
    if booking_data.guests > property_obj.max_guests:
        raise ValueError(
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
        raise ValueError(
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
        guest_name=booking_data.guest_name,
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
) -> models.Booking | None:

    statement = select(models.Booking).where(
        models.Booking.id == booking_id
    )

    return db.execute(
        statement
    ).scalar_one_or_none()


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

def cancel_booking(
    db: Session,
    booking_id: int,
) -> models.Booking | None:

    booking = get_booking(
        db=db,
        booking_id=booking_id,
    )

    if booking is None:
        return None

    if booking.status == "CANCELLED":
        raise ValueError(
            "Booking is already cancelled"
        )

    if booking.status != "PENDING":
        raise ValueError(
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