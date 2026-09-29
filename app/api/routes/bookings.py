from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import BookingCreate, BookingResponse
from app.services.booking_service import (
    cancel_booking,
    create_booking,
    get_booking,
    get_property_bookings,
    get_user_bookings,
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
    current_user: models.User = Depends(get_current_user),
):
    return create_booking(
        db=db,
        booking_data=booking_data,
        user_id=current_user.id,
    )


@router.get(
    "/me",
    response_model=list[BookingResponse],
)
def get_my_bookings_endpoint(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return get_user_bookings(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
)
def get_booking_endpoint(
    booking_id: int,
    db: Session = Depends(get_db),
):
    return get_booking(
        db=db,
        booking_id=booking_id,
    )


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
    current_user: models.User = Depends(get_current_user),
):
    return cancel_booking(
        db=db,
        booking_id=booking_id,
        user_id=current_user.id,
    )