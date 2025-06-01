from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate
from typing import Dict

from microservice.models import UserData, UserResponse, AppStatus
from microservice.db import users_db, support_info

router = APIRouter()

users: Dict[int, UserData] = {}

@router.get("/status", response_model=AppStatus, status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=bool(users))

@router.get("/api/users/{user_id}", response_model=UserResponse, status_code=HTTPStatus.OK)
def get_user(user_id: int) -> UserResponse:
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(data=user, support=support_info)

@router.post("/api/users/", response_model=UserData, status_code=HTTPStatus.OK)
def create_user(user: UserData) -> UserData:
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.id] = user
    return user

@router.get("/api/users/", response_model=Page[UserData], status_code=HTTPStatus.OK)
def get_all_users() -> Page:
    return paginate(list(users_db.values()))