from main import main
from fastapi import Depends
from main.schemas.response import DefaultResponse
from main.schemas.user import UserRegular
from main.utils.user import get_current_user


@main.get('/api/users/me', response_model=DefaultResponse)
async def api_users_me(user: UserRegular = Depends(get_current_user)):
    return {
        'result': True,
        'message': 'Успех',
        'data': UserRegular(id=user.id, username=user.username, avatar=user.avatar, online=user.online)
    }
