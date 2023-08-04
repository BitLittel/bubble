from pydantic import BaseModel


class DefaultResponse(BaseModel):
    result: bool
    message: str
    data: dict
