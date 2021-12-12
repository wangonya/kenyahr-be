from pydantic.networks import EmailStr

from app.models import BaseModel, PydanticBaseModel


class User(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = False
    email_verified: bool = False


class UserCreate(PydanticBaseModel):
    username: str
    email: EmailStr
    password: str


class UserInDB(User):
    password: str


class Token(PydanticBaseModel):
    access_token: str
    token_type: str
