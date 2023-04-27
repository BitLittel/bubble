from pydantic import BaseModel
from main.schemas.user_model import UserRegular


class DefaultResponse(BaseModel):
    result: bool
    message: str
    data: dict | UserRegular
