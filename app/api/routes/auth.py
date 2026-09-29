from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserCreate, UserResponse,UserLogin,TokenResponse
from app.services.auth_service import register_user,login_user
from app import models
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        return register_user(
            db=db,
            user_data=user_data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    try:
        access_token = login_user(
            db=db,
            email=user_data.email,
            password=user_data.password,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=401,
            detail=str(exc),
        )

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: models.User = Depends(
        get_current_user
    ),
):
    return current_user