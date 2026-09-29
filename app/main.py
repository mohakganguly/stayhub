from fastapi import FastAPI,Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import engine, Base,get_db
from app import models
from pydantic import BaseModel, Field
from app.api.routes.bookings import router as booking_router
from app.api.routes.listings import router as listing_router


class PropertyCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=1000)
    location: str = Field(min_length=2, max_length=100)
    price: int = Field(gt=0)
    max_guests: int = Field(default=2, gt=0, le=20)

app=FastAPI()

app.include_router(listing_router)
app.include_router(booking_router)

from app.database import engine


@app.get("/db-test")
def db_test():
    with engine.connect() as connection:
        return {"database": "connected"}

@app.get("/")
def home():
    return {"message": "Welcome to StayHub"}

@app.get("/health")
def health():
    return {"status":"healthy"}


@app.get("/properties/{property_id}")
def get_property(
    property_id: int,
    db: Session = Depends(get_db),
):
    property = (
        db.query(models.Property)
        .filter(models.Property.id == property_id)
        .first()
    )

    if property is None:
        return {"error": "Property not found."}

    return property

@app.get("/properties")
def get_properties(
    location: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Property)

    if location:
        query = query.filter(
            models.Property.location.ilike(location)
        )

    if min_price is not None:
        query = query.filter(
            models.Property.price >= min_price
        )

    if max_price is not None:
        query = query.filter(
            models.Property.price <= max_price
        )

    return query.all()

@app.post("/properties")
def create_property(
    property: PropertyCreate,
    db: Session = Depends(get_db),
):
    new_property = models.Property(
        title=property.title,
        description=property.description,
        location=property.location,
        price=property.price,
        max_guests=property.max_guests,
    )

    db.add(new_property)
    db.commit()
    db.refresh(new_property)

    return new_property

@app.get("/db-properties")
def get_db_properties(db: Session = Depends(get_db)):
    return db.query(models.Property).all()