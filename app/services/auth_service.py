from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.schemas import UserCreate
from app.security import (
    hash_password,
    create_access_token,
    verify_password,
)
from app.exceptions import ConflictError

def register_user(
    db: Session,
    user_data: UserCreate,
) -> models.User:

    existing_user = db.execute(
        select(models.User).where(
            models.User.email == user_data.email
        )
    ).scalar_one_or_none()

    if existing_user is not None:
        raise ConflictError(
            "Email is already registered"
        )

    user = models.User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(
            user_data.password
        ),
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    except Exception:
        db.rollback()
        raise

def login_user(
    db: Session,
    email: str,
    password: str,
) -> str:

    user = db.execute(
        select(models.User).where(
            models.User.email == email
        )
    ).scalar_one_or_none()

    if user is None:
        raise ValueError(
            "Invalid email or password"
        )

    if not verify_password(
        password,
        user.password_hash,
    ):
        raise ValueError(
            "Invalid email or password"
        )

    return create_access_token(
        user_id=user.id
    )