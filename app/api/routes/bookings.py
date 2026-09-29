from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import BookingCreate, BookingResponse
from app.services.booking_service import (
    create_booking,
    get_booking,
    get_property_bookings,
    cancel_booking,
)


router = APIRouter(
    prefix="/api/v1/bookings",
    tags=["Bookings"],
)


@router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_booking_endpoint(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_booking(
            db=db,
            booking_data=booking_data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
)
def get_booking_endpoint(
    booking_id: int,
    db: Session = Depends(get_db),
):
    booking = get_booking(
        db=db,
        booking_id=booking_id,
    )

    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    return booking

@router.get(
    "/property/{property_id}",
    response_model=list[BookingResponse],
)
def get_property_bookings_endpoint(
    property_id: int,
    db: Session = Depends(get_db),
):
    return get_property_bookings(
        db=db,
        property_id=property_id,
    )

@router.patch(
    "/{booking_id}/cancel",
    response_model=BookingResponse,
)
def cancel_booking_endpoint(
    booking_id: int,
    db: Session = Depends(get_db),
):
    try:
        booking = cancel_booking(
            db=db,
            booking_id=booking_id,
        )

        if booking is None:
            raise HTTPException(
                status_code=404,
                detail="Booking not found",
            )

        return booking

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )