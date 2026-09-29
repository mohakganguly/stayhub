from pydantic import BaseModel, ConfigDict, Field, model_validator
from datetime import date


class PropertyImageCreate(BaseModel):
    image_url: str = Field(min_length=1, max_length=500)
    position: int = Field(default=0, ge=0)


class PropertyCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=1000)
    location: str = Field(min_length=2, max_length=150)
    price_per_night: int = Field(gt=0)
    max_guests: int = Field(default=2, gt=0, le=20)
    rating: float = Field(default=0.0, ge=0, le=5)
    category: str = Field(min_length=2, max_length=50)

    images: list[PropertyImageCreate] = []


class PropertyImageResponse(BaseModel):
    id: int
    image_url: str
    position: int

    model_config = ConfigDict(from_attributes=True)


class PropertyResponse(BaseModel):
    id: int
    title: str
    description: str
    location: str
    price_per_night: int
    max_guests: int
    rating: float
    category: str
    images: list[PropertyImageResponse]=Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

class PaginatedListingsResponse(BaseModel):
    items: list[PropertyResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

class PropertyUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        min_length=10,
        max_length=1000,
    )

    location: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    price_per_night: int | None = Field(
        default=None,
        gt=0,
    )

    max_guests: int | None = Field(
        default=None,
        gt=0,
        le=20,
    )

    rating: float | None = Field(
        default=None,
        ge=0,
        le=5,
    )

    category: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )


class BookingCreate(BaseModel):
    property_id: int = Field(gt=0)

    guest_name: str = Field(
        min_length=2,
        max_length=100,
    )

    check_in: date
    check_out: date

    guests: int = Field(
        gt=0,
        le=20,
    )

    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_in >= self.check_out:
            raise ValueError(
                "check_out must be after check_in"
            )

        return self


class BookingResponse(BaseModel):
    id: int
    property_id: int
    guest_name: str
    check_in: date
    check_out: date
    guests: int
    total_price: int
    status: str

    model_config = ConfigDict(
        from_attributes=True
    )