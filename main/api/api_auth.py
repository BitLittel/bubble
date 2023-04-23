from pydantic import BaseModel, EmailStr, Field, UUID4
from main import main
from uuid import uuid4
from datetime import datetime, timedelta
from fastapi import status, Request, Response, Cookie
from sqlalchemy import and_
from main.models.database import Session, hash_password, Users, Tokens
from fastapi import Depends, HTTPException
from main import config


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


async def update_token(user_id: int) -> uuid4:
    with Session() as db:
        check_token = db.query(Tokens).filter(and_(Tokens.user_id == user_id, Tokens.type == 'regular')).first()
        if check_token is not None:
            if check_token.expires < datetime.now():
                check_token.expires = datetime.now() + timedelta(weeks=2)
                new_token = uuid4()
                check_token.token = new_token
                check_token.datetime_create = datetime.now()
                db.commit()
                return new_token
            else:
                return check_token.token
        else:
            new_token = Tokens(
                type='regular',
                user_id=user_id,
                expires=datetime.now() + timedelta(weeks=2)
            )
            db.add(new_token)
            db.commit()
            return new_token.token


@main.post('/login')
async def login(user: UserLogin, response: Response):
    with Session() as db:
        get_user = db.query(Users).filter(and_(
            Users.username == user.username,
            Users.is_active == True
        )).first()
        if get_user is not None:
            if get_user.verify_password(user.password):
                check_token = await update_token(get_user.id)
                response.set_cookie(key='token', value=check_token, httponly=True)
                return {'status': 'ok'}
        raise HTTPException(status_code=400, detail="Incorrect email or password")


@main.post('/signup')
async def signup(user: UserSignUp):
    with Session() as db:
        print(user.username, user.password, user.email)
        if await get_user_by_username(username=user.username):
            raise HTTPException(status_code=409, detail="This username already exist")

        if await get_user_by_email(email=user.email):
            raise HTTPException(status_code=409, detail="This email already exist")

        new_user = Users(
            username=user.username,
            password=hash_password(user.password),
            email=user.email,
            avatar=config.DEFAULT_AVATAR
        )
        db.add(new_user)
        db.commit()

        new_token = Tokens(
            type='activate',
            user_id=new_user.id,
            expires=datetime.now() + timedelta(weeks=1)
        )
        db.add(new_token)
        db.commit()
        return {'status': 'ok', 'link': f'{config.MAIN_URL}/activate/{new_token.token}'}


@main.get('/activate/{token}')
async def activate_by_token(token: UUID4):
    check_token = await get_user_by_token_with_type(token=token, type_token='activate')
    if check_token:
        with Session() as db:
            user = db.query(Users).filter(Users.id == check_token.id).first()
            user.is_active = True
            db.commit()
            return {'status': 'ok', 'message': 'Your account is activate'}
    else:
        raise HTTPException(status_code=404, detail="This token not found")


@main.get('/users/me')
async def get_user(user: UserRegular = Depends(get_current_user)):
    return user
