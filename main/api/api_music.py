from main import main
from main.models.database import query_execute
from fastapi.responses import FileResponse, StreamingResponse
from fastapi import HTTPException, Request
from main.utils.music import range_requests_response


@main.get("/api/music_download")
def api_music_download():
    return FileResponse(path='data.xlsx', filename='Статистика покупок.xlsx', media_type='multipart/form-data')
# todo: Изучить вопрос с FileResponse и понять какие есть ещё media_type


@main.get("/api/music/{id_music}")
async def api_get_music(id_music: int, request: Request) -> StreamingResponse:
    get_music = await query_execute(
        query_text=f'select * from "Musics" as M where M.id = {id_music}',
        fetch_all=False,
        type_query='read'
    )
    if get_music is None:
        raise HTTPException(404, detail="Трек не найден")

    return range_requests_response(request, file_name=get_music.filename, content_type="audio/mpeg")
