import os
from main import main
from main import config
from main.models.database import query_execute
from fastapi.responses import StreamingResponse


async def open_image(file_path):
    with open(file_path, 'rb') as f:
        yield f.read()


@main.get("/api/image/{id_image}")
async def api_get_images(id_image: int):
    if id_image == 1:
        file_path = os.path.join(config.MAIN_PATH, 'static', 'img', "default_img.jpg")
        return StreamingResponse(
            open_image(file_path),
            headers={'content-type': 'image/jpeg'},
            status_code=200
        )

    get_image = await query_execute(
        query_text=f'select * from "Images" as I where I.id = {id_image}',
        fetch_all=False,
        type_query='read'
    )

    if get_image is None:
        file_path = os.path.join(config.PHOTOS_FOLDER, "default_img.jpg")
        return StreamingResponse(
            open_image(file_path),
            headers={'content-type': 'image/jpeg'},
            status_code=200
        )
    else:
        file_path = os.path.join(config.PHOTOS_FOLDER, get_image.file_name)
        return StreamingResponse(
            open_image(file_path),
            headers={'content-type': get_image.content_type},
            status_code=200
        )
