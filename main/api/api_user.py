from main import main
from fastapi import Depends
from main.schemas.user import UserRegular, ResponseUserRegular
from main.utils.user import get_current_user


@main.get('/api/users/me', response_model=ResponseUserRegular)
async def api_users_me(user: UserRegular = Depends(get_current_user)):
    return {'result': True, 'message': 'Успех', 'data': user}
