from pydantic import UUID4
from datetime import datetime
from fastapi import Cookie
from sqlalchemy import and_
from main.models.database import Session, Users, Tokens
from fastapi import HTTPException
from sqlalchemy import text
from main.schemas.user_model import UserRegular


async def get_user_by_username(username: str) -> UserRegular | bool:
    async with Session() as db:
        user = await db.query(Users).filter(Users.username == username).first()
        if user is not None:
            return UserRegular(id=user.id, username=user.username, avatar=user.avatar, online=user.online)
        return False


async def get_user_by_email(email: str) -> UserRegular | bool:
    async with Session() as db:
        user = await db.query(Users).filter(Users.email == email).first()
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
    async with Session() as db:

        token_user = await db.execute(
            text(f'select * '
                 f'from "Tokens" as T '
                 f'where T.token = \'{token}\' and T.type = \'{type_token}\' and T.expires > \'{datetime.now()}\'')
        )
        token_user = token_user.fetchone()

        # todo: Ебать, всё нахуй переписывать на эту говнину с execute, надо чёт придумать чтобы было каеф
        # todo: ну радует хотябы что теперь реально async, даже SQLalchemy

        print(token_user)
        if token_user is not None:
            user = await db.execute(text(f'select * from "Users" as U where U.id = {token_user.user_id}'))
            user = user.fetchone()

            if type_token == 'activate':

                db.query(Tokens).filter(Tokens.token == token).delete()
                db.commit()

            return UserRegular(id=user.id, username=user.username, avatar=user.avatar, online=user.online)
        return False
