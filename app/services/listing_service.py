from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select,func
from app import models
from app.schemas import PropertyCreate, PropertyUpdate


def create_listing(
    db: Session,
    listing: PropertyCreate,
) -> models.Property:

    try:
        property_obj = models.Property(
            title=listing.title,
            description=listing.description,
            location=listing.location,
            price_per_night=listing.price_per_night,
            max_guests=listing.max_guests,
            rating=listing.rating,
            category=listing.category,
        )

        for image in listing.images:
            property_obj.images.append(
                models.PropertyImage(
                    image_url=image.image_url,
                    position=image.position,
                )
            )

        db.add(property_obj)

        db.commit()
        db.refresh(property_obj)

        return property_obj

    except Exception:
        db.rollback()
        raise


def get_listing(
    db: Session,
    listing_id: int,
) -> models.Property | None:

    statement = (
        select(models.Property)
        .options(joinedload(models.Property.images))
        .where(models.Property.id == listing_id)
    )

    result = db.execute(statement)

    return result.unique().scalar_one_or_none()


def get_listings(
    db: Session,
    location: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    sort: str = "newest",
    page: int = 1,
    page_size: int = 20,
):
    # -------------------------
    # Build reusable filters
    # -------------------------

    conditions = []

    if location:
        conditions.append(
            models.Property.location.ilike(
                f"%{location}%"
            )
        )

    if min_price is not None:
        conditions.append(
            models.Property.price_per_night >= min_price
        )

    if max_price is not None:
        conditions.append(
            models.Property.price_per_night <= max_price
        )

    # -------------------------
    # Base listing query
    # -------------------------

    statement = (
        select(models.Property)
        .options(
            joinedload(models.Property.images)
        )
        .where(*conditions)
    )

    # -------------------------
    # Sorting
    # -------------------------

    sort_options = {
        "price_asc": models.Property.price_per_night.asc(),
        "price_desc": models.Property.price_per_night.desc(),
        "rating": models.Property.rating.desc(),
        "newest": models.Property.created_at.desc(),
    }

    if sort not in sort_options:
        raise ValueError("Invalid sort option")

    statement = statement.order_by(
        sort_options[sort]
    )

    # -------------------------
    # Count query
    # -------------------------

    count_statement = (
        select(func.count())
        .select_from(models.Property)
        .where(*conditions)
    )

    total = db.execute(
        count_statement
    ).scalar_one()

    # -------------------------
    # Pagination
    # -------------------------

    offset = (page - 1) * page_size

    statement = (
        statement
        .offset(offset)
        .limit(page_size)
    )

    # -------------------------
    # Execute listing query
    # -------------------------

    result = db.execute(statement)

    properties = (
        result
        .unique()
        .scalars()
        .all()
    )

    total_pages = (
        total + page_size - 1
    ) // page_size

    return {
        "items": properties,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }

def delete_listing(
    db: Session,
    listing_id: int,
) -> bool:

    listing = get_listing(db, listing_id)

    if listing is None:
        return False

    try:
        db.delete(listing)
        db.commit()

        return True

    except Exception:
        db.rollback()
        raise

def update_listing(
    db: Session,
    listing_id: int,
    listing_data: PropertyUpdate,
) -> models.Property | None:

    listing = get_listing(db, listing_id)

    if listing is None:
        return None

    try:
        update_data = listing_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(listing, field, value)

        db.commit()
        db.refresh(listing)

        return listing

    except Exception:
        db.rollback()
        raise