from main import main
from main.schemas.user import UserRegular
from main.utils.user import get_current_user
from fastapi.responses import StreamingResponse
from main.utils.upload import load_and_save_file
from fastapi import Depends, UploadFile, HTTPException
from main.schemas.file import FileResponse


@main.post('/api/upload_file', status_code=202, response_model=FileResponse)
async def work(
        file: list[UploadFile],
        action: str = 'music',
        user: UserRegular = Depends(get_current_user),
        music_id: int = None
) -> StreamingResponse:

    if action not in ['music', 'avatar', 'cover']:
        raise HTTPException(406, detail="Получен не корректный action")

    return StreamingResponse(load_and_save_file(file, action, user.id, music_id), status_code=202)
