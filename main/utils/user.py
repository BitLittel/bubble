from pydantic import UUID4
from datetime import datetime
from fastapi import Cookie
from sqlalchemy import and_
from main.models.database import Session, Users, Tokens
from fastapi import HTTPException
from main.schemas.user_model import UserRegular


async def get_user_by_username(username: str) -> UserRegular | bool:
    with Session() as db:
        user = db.query(Users).filter(Users.username == username).first()
        if user is not None:
            return UserRegular(id=user.id, username=user.username, avatar=user.avatar, online=user.online)
        return False


async def get_user_by_email(email: str) -> UserRegular | bool:
    with Session() as db:
        user = db.query(Users).filter(Users.email == email).first()
        if user is not None:
            return UserRegular(id=user.id, username=user.username, avatar=user.avatar, online=user.online)
        return False


async def get_current_user(token=Cookie()):
    if token is not None or token != '':
        user = await get_user_by_token_with_type(token=token, type_token='regular')
        if user:
            return user
    raise HTTPException(status_code=401, detail="Unauthorized")


async def get_user_by_token_with_type(token: UUID4, type_token: str) -> UserRegular | bool:
    with Session() as db:
        token = db.query(Tokens).filter(
            and_(Tokens.token == token, Tokens.type == type_token, Tokens.expires > datetime.now())
        ).first()
        if token is not None:
            user = db.query(Users).filter(Users.id == token.user_id).first()
            return UserRegular(id=user.id, username=user.username, avatar=user.avatar, online=user.online)
        return False
