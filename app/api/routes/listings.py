
from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from app import models
from app.database import get_db
from app.schemas import(
PropertyCreate,
PropertyResponse,
 PaginatedListingsResponse,
 PropertyUpdate
) 
from app.services.listing_service import (
create_listing, 
get_listing,
get_listings,
delete_listing,
update_listing,
)

router = APIRouter(
    prefix="/api/v1/listings",
    tags=["Listings"],
)


@router.get(
    "",
    response_model=PaginatedListingsResponse,
)
def get_listings_endpoint(
    location: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    sort: str = Query(default="newest"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    try:
        return get_listings(
            db=db,
            location=location,
            min_price=min_price,
            max_price=max_price,
            sort=sort,
            page=page,
            page_size=page_size,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post(
    "",
    response_model=PropertyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_listing_endpoint(
    listing: PropertyCreate,
    db: Session = Depends(get_db),
):
    return create_listing(db, listing)

@router.get(
    "/{listing_id}",
    response_model=PropertyResponse,
)
def get_listing_endpoint(
    listing_id: int,
    db: Session = Depends(get_db),
):
    listing = get_listing(db, listing_id)

    if listing is None:
        raise HTTPException(
            status_code=404,
            detail="Listing not found",
        )

    return listing

@router.delete(
    "/{listing_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_listing_endpoint(
    listing_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_listing(
        db=db,
        listing_id=listing_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Listing not found",
        )

    return None

@router.patch(
    "/{listing_id}",
    response_model=PropertyResponse,
)
def update_listing_endpoint(
    listing_id: int,
    listing_data: PropertyUpdate,
    db: Session = Depends(get_db),
):
    listing = update_listing(
        db=db,
        listing_id=listing_id,
        listing_data=listing_data,
    )

    if listing is None:
        raise HTTPException(
            status_code=404,
            detail="Listing not found",
        )

    return listing