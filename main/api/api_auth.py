from pydantic import UUID4
from main import main
from uuid import uuid4
from datetime import datetime, timedelta
from fastapi import Response
from sqlalchemy import and_
from main.models.database import Session, hash_password, Users, Tokens
from fastapi import Depends, HTTPException
from main import config
from main.schemas.response_model import DefaultResponse
from main.schemas.user_model import UserRegular, UserLogin, UserSignUp
from main.utils.user import get_user_by_username, get_user_by_email, get_current_user, get_user_by_token_with_type


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


@main.post('/login', response_model=DefaultResponse)
async def login(user: UserLogin, response: Response):
    with Session() as db:
        user_login = db.query(Users).filter(and_(
            Users.username == user.username,
            Users.is_active == True
        )).first()
        if user_login is not None:
            if user_login.verify_password(user.password):
                token = await update_token(user_login.id)
                response.set_cookie(key='token', value=token, httponly=True, samesite="strict", max_age=1209600)
                return {
                    'result': True,
                    'message': 'Успех',
                    'data': UserRegular(
                        id=user_login.id,
                        username=user_login.username,
                        avatar=user_login.avatar,
                        online=user_login.online
                    )
                }
        raise HTTPException(status_code=400, detail="Incorrect username or password")


@main.post('/signup', response_model=DefaultResponse)
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
        return {
            'result': True,
            'message': 'Успех',
            'data': f'{config.MAIN_URL}/activate/{new_token.token}'
        }


@main.get('/activate/{token}', response_model=DefaultResponse)
async def activate_by_token(token: UUID4):
    check_token = await get_user_by_token_with_type(token=token, type_token='activate')
    if check_token:
        with Session() as db:
            user = db.query(Users).filter(Users.id == check_token.id).first()
            user.is_active = True
            db.commit()
            return {
                'result': True,
                'message': 'Вы активировали аккаунт',
                'data': {}
            }
    else:
        raise HTTPException(status_code=404, detail="This code not found")


@main.get('/users/me', response_model=DefaultResponse)
async def get_user(user: UserRegular = Depends(get_current_user)):
    return {
        'result': True,
        'message': 'Успех',
        'data': UserRegular(
            id=user.id,
            username=user.username,
            avatar=user.avatar,
            online=user.online
        )
    }


@main.get("/logout", response_model=DefaultResponse)
async def logout(response: Response):
    response.delete_cookie(key='token')
    return {'result': True, 'message': 'Вы успешно вышли', 'data': {}}
