from pydantic import UUID4
from main import main
from uuid import uuid4
from datetime import datetime, timedelta
from main.models.database import query_execute, hash_password
from fastapi import Depends, HTTPException, Response, responses
from main import config
from main.schemas.response_model import DefaultResponse
from main.schemas.user_model import UserRegular, UserLogin, UserSignUp
from main.utils.user import get_user_by_username, get_user_by_email, get_current_user, get_user_by_token_with_type


async def update_token(user_id: int) -> uuid4:
    check_token = await query_execute(
        query_text=f'select * from "Tokens" as T where T.user_id = {user_id} and T.type = \'regular\'',
        fetch_all=False,
        type_query='read'
    )
    if check_token is not None:
        if check_token.expires < datetime.now():
            new_token = uuid4()
            await query_execute(
                query_text=f'update "Tokens" as T '
                           f'set (expires, token, datetime_create) = '
                           f'(\'{datetime.now() + timedelta(weeks=2)}\', \'{new_token}\', \'{datetime.now()}\') '
                           f'where T.user_id = {user_id} and T.type = \'regular\'',
                fetch_all=False,
                type_query='update'
            )
            return new_token
        else:
            return check_token.token
    else:
        await query_execute(
            query_text=f'insert into "Tokens" (type, expires, user_id, datetime_create) '
                       f'VALUES (\'regular\', \'{datetime.now() + timedelta(weeks=2)}\', '
                       f'{user_id}, \'{datetime.now()}\')',
            fetch_all=False,
            type_query='insert'
        )
        get_new_token = await query_execute(
            query_text=f'select * from "Tokens" as T where T.user_id = {user_id} and T.type = \'regular\'',
            fetch_all=False,
            type_query='read'
        )
        return get_new_token.token


@main.post('/login', response_model=DefaultResponse)
async def login(user: UserLogin, response: Response):
    user_login = await query_execute(
        query_text=f'select * from "Users" as U where U.username = \'{user.username}\' and U.is_active = true',
        fetch_all=False,
        type_query='read'
    )

    if user_login is not None:
        if user_login.password == hash_password(user.password):
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
    if await get_user_by_username(username=user.username):
        raise HTTPException(status_code=409, detail="This username already exist")

    if await get_user_by_email(email=user.email):
        raise HTTPException(status_code=409, detail="This email already exist")

    await query_execute(
        query_text=f'insert into "Users" (username, password, email, avatar, online, is_active) '
                   f'values (\'{user.username}\', \'{hash_password(user.password)}\', '
                   f'\'{user.email}\', \'{config.DEFAULT_AVATAR}\', false, false)',
        fetch_all=False,
        type_query='insert'
    )

    get_new_user = await get_user_by_email(user.email)

    new_token_gen = uuid4()
    await query_execute(
        query_text=f'insert into "Tokens" (type, user_id, expires, token, datetime_create) '
                   f'values (\'activate\', {get_new_user.id}, \'{datetime.now() + timedelta(weeks=1)}\', '
                   f'\'{new_token_gen}\', \'{datetime.now()}\')',
        fetch_all=False,
        type_query='insert'
    )

    return DefaultResponse(
        result=True,
        message=f'Вам на почту отправлено письмо для активации аккаунта. http://127.0.0.1:8000/?token={new_token_gen}',
        data={}
    )


@main.post('/activate/{token}', response_model=DefaultResponse)
async def activate_by_token(token: UUID4, response: Response):
    check_token = await get_user_by_token_with_type(token=token, type_token='activate')
    if check_token:
        await query_execute(
            query_text=f'update "Users" as U set is_active = true where U.id = {check_token.id}',
            fetch_all=False,
            type_query='update'
        )
        token = await update_token(check_token.id)

        user_login = await get_user_by_token_with_type(token=token, type_token='regular')

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
    else:
        raise HTTPException(status_code=404, detail="This code not found")


@main.get('/users/me', response_model=DefaultResponse)
async def get_user(user: UserRegular = Depends(get_current_user)):
    return {
        'result': True,
        'message': 'Успех',
        'data': UserRegular(id=user.id, username=user.username, avatar=user.avatar, online=user.online)
    }


@main.get("/logout", response_model=DefaultResponse)
async def logout(response: Response):
    response.delete_cookie(key='token')
    return responses.RedirectResponse('/')
