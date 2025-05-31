from fastapi import APIRouter, HTTPException
from typing import Dict

from microservice.models import UserData, UserResponse
from microservice.db import users_db, support_info

router = APIRouter()

@router.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int) -> UserResponse:
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(data=user, support=support_info)

@router.post("/api/users/", response_model=UserData)
def create_user(user: UserData) -> UserData:
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.id] = user
    return user

@router.get("/api/users/", response_model=Dict[int, UserData])
def list_users() -> Dict[int, UserData]:
    return users_db