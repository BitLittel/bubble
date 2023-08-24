from pydantic import BaseModel, EmailStr, Field
from main.schemas.response import DefaultResponse


class UserSignUp(BaseModel):
    username: str = Field(pattern=r'^([a-zA-Z0-9_-|\\\/?.()*%$#@!<>{}\[\]]){5,25}$')
    password: str = Field(pattern=r'^([a-zA-Z0-9_]|\W){8,64}$')
    email: EmailStr


class UserLogin(BaseModel):
    username: str = Field(pattern=r'^([a-zA-Z0-9_-|\\\/?.()*%$#@!<>{}\[\]]){5,25}$')
    password: str = Field(pattern=r'^([a-zA-Z0-9_]|\W){8,64}$')


class UserRegular(BaseModel):
    id: int
    username: str
    avatar: str
    online: bool
    liked_playlist: list


class ResponseUserRegular(DefaultResponse):
    data: UserRegular
