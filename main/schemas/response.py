from pydantic import BaseModel
from main.schemas.user import UserRegular


class DefaultResponse(BaseModel):
    result: bool
    message: str
    data: dict | UserRegular
