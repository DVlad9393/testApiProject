from pydantic import BaseModel, EmailStr, HttpUrl

class UserData(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl

class SupportData(BaseModel):
    url: HttpUrl
    text: str

class UserResponse(BaseModel):
    data: UserData
    support: SupportData

class AppStatus(BaseModel):
    users: bool