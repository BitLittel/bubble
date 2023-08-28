from pydantic import UUID4
from main import main
from uuid import uuid4
from main.utils.another import escape
from datetime import datetime, timedelta
from main.models.database import query_execute, hash_password
from fastapi import HTTPException, Response
from main import config
from main.schemas.response import DefaultResponse
from main.schemas.user import UserRegular, UserLogin, UserSignUp, ResponseUserRegular
from main.utils.user import get_user_by_username, get_user_by_email, get_user_by_token_with_type


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


@main.post('/api/login', response_model=ResponseUserRegular)
async def api_login(user: UserLogin, response: Response):
    user_login = await query_execute(
        query_text=f'select '
                   f'U.id, '
                   f'U.username, '
                   f'CONCAT(\'{config.MAIN_URL}/api/image/\', I.id) as avatar, '
                   f'U.online,'
                   f'U.liked_playlist, '
                   f'U.password '
                   f'from "Users" as U '
                   f'left join "Images" as I on I.id = U.avatar '
                   f'where U.username = \'{user.username}\' and U.is_active = true',
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
                    online=user_login.online,
                    liked_playlist=user_login.liked_playlist
                )
            }
    raise HTTPException(status_code=400, detail="Не верное имя пользователя или пароль")


@main.post('/api/signup', response_model=DefaultResponse)
async def api_signup(user: UserSignUp):
    if await get_user_by_username(username=user.username):
        raise HTTPException(status_code=409, detail="Это имя пользователя уже занято")

    if await get_user_by_email(email=user.email):
        raise HTTPException(status_code=409, detail="Эта почта уже занята")
    # Регистрируем пользователя
    await query_execute(
        query_text=f'insert into "Users" (username, password, email, avatar, online, is_active, liked_playlist) '
                   f'values (\'{escape(user.username)}\', \'{hash_password(user.password)}\', '
                   f'\'{escape(user.email)}\', 1, false, false, ARRAY[]::bigint[])',
        fetch_all=False,
        type_query='insert'
    )

    get_new_user = await get_user_by_email(user.email)
    # Создаём токен для активации аккаунта
    new_token_gen = uuid4()
    await query_execute(
        query_text=f'insert into "Tokens" (type, user_id, expires, token, datetime_create) '
                   f'values (\'activate\', {get_new_user.id}, \'{datetime.now() + timedelta(weeks=1)}\', '
                   f'\'{new_token_gen}\', \'{datetime.now()}\')',
        fetch_all=False,
        type_query='insert'
    )
    # Создаём дефолтный плейлист, где будет храниться вся музыка пользователя
    await query_execute(
        query_text=f'insert into "PlayLists" (name, cover, datetime_add, user_id) '
                   f'values (\'Вся моя музыка\', 1, \'{datetime.now()}\', '
                   f'{get_new_user.id})',
        fetch_all=False,
        type_query='insert'
    )

    default_playlist = await query_execute(
        query_text=f'select * from "PlayLists" as PL '
                   f'where PL.name = \'Вся моя музыка\' and PL.user_id = {get_new_user.id}',
        fetch_all=False,
        type_query='read'
    )
    # append default playlist id in liked_playlist array
    await query_execute(
        query_text=f'update "Users" '
                   f'set liked_playlist =  array_append(liked_playlist, {default_playlist.id}::bigint) '
                   f'where id = {get_new_user.id}',
        fetch_all=False,
        type_query='update'
    )
    # remove playlist id in liked_playlist array
    # update "Users"
    # set liked_playlist = (select
    #     array_remove(U.liked_playlist, 12)
    # from "Users" as U
    # where U.id = 11)
    # where id = 11

    return {
        'result': True,
        'message': f'Вам на почту отправлено письмо для активации аккаунта. '
                   f'{config.MAIN_URL}/?token={new_token_gen}',
        'data': {}
    }


@main.post('/activate/{token}', response_model=ResponseUserRegular)
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
            'data': user_login
        }
    else:
        raise HTTPException(status_code=404, detail="Код не найден")


@main.post("/api/logout", response_model=DefaultResponse)
async def logout(response: Response):
    response.delete_cookie(key='token')
    return {'result': True, 'message': 'Выход выполнен успешно', 'data': {}}
