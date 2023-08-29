# from pydantic import UUID4
from main import main
from fastapi import Depends
from main.schemas.user import UserRegular
from main.utils.user import get_current_user


@main.get("/api/friends")
async def api_get_all_playlist(user: UserRegular = Depends(get_current_user)):
    print(user)
    return {
        'result': True,
        'message': 'Успех',
        'data': {
            'friends': []
        }
    }
