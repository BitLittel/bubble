from pydantic import BaseModel, EmailStr, Field


class UserSignUp(BaseModel):
    username: str
    password: str = Field(..., regex="((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})")
    email: EmailStr


class UserLogin(BaseModel):
    username: str
    password: str = Field(..., regex="((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})")


class UserRegular(BaseModel):
    id: int
    username: str
    avatar: str
    online: bool
