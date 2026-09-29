from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    CheckConstraint,
    Date,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        UniqueConstraint(
            "email",
            name="uq_users_email",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(100),
        nullable=False,
    )

    email = Column(
        String(255),
        nullable=False,
        index=True,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    bookings = relationship(
        "Booking",
        back_populates="user",
    )


class Property(Base):
    __tablename__ = "properties"
    __table_args__ = (
        CheckConstraint(
            "price_per_night > 0",
            name="ck_properties_price_positive",
        ),
        CheckConstraint(
            "max_guests > 0",
            name="ck_properties_max_guests_positive",
        ),
        CheckConstraint(
            "rating >= 0 AND rating <= 5",
            name="ck_properties_rating_range",
        ),
    )
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)

    location = Column(String(150), nullable=False, index=True)

    price_per_night = Column(Integer, nullable=False, index=True)

    max_guests = Column(Integer, nullable=False, default=2)

    rating = Column(Float, nullable=False, default=0.0, index=True)

    category = Column(String(50), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    images = relationship(
        "PropertyImage",
        back_populates="property",
        cascade="all, delete-orphan",
    )

    bookings=relationship(
        "Booking",
        back_populates="property",
    )


class PropertyImage(Base):
    __tablename__ = "property_images"

    id = Column(Integer, primary_key=True, index=True)

    property_id = Column(
        Integer,
        ForeignKey("properties.id"),
        nullable=False,
    )

    image_url = Column(String(500), nullable=False)

    position = Column(Integer, nullable=False, default=0)

    property = relationship(
        "Property",
        back_populates="images",
    )

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    property_id = Column(
        Integer,
        ForeignKey("properties.id"),
        nullable=False,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )
    check_in = Column(
        Date,
        nullable=False,
    )

    check_out = Column(
        Date,
        nullable=False,
    )

    guests = Column(
        Integer,
        nullable=False,
    )

    total_price = Column(
        Integer,
        nullable=False,
    )

    status = Column(
        String(20),
        nullable=False,
        default="PENDING",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    property = relationship(
        "Property",
        back_populates="bookings",
    )
    user = relationship(
        "User",
        back_populates="bookings",
    )