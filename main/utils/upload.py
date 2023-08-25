import os
import aiofiles
import audioread
from uuid import uuid4
from main import config
from tinytag import TinyTag
from datetime import datetime
from fastapi import HTTPException
from main.schemas.music import Music
from main.utils.another import escape
from main.models.database import Session
from sqlalchemy import text
from main.models.database import query_execute
from main.schemas.file import FileResponse, File, Photo


async def validate_file(file_, action_):
    if len(file_) > 1:
        raise HTTPException(406, detail="Получено более одного файла")
    file = file_[0]

    # get file_size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    await file.seek(0)
    if file_size > config.MAX_FILE_SIZE:
        raise HTTPException(406, detail="Получен большой файл")

    # Проверяем content_type
    content_type = file.content_type
    print(f'CONTENT_TYPE: {content_type}')
    if action_ in ['photo', 'cover']:
        if content_type not in config.PHOTO_FORMAT:
            raise HTTPException(406, detail="Получен не корректный формат данных")
    if action_ == 'music':
        if content_type not in config.AUDIO_FORMAT:
            raise HTTPException(406, detail="Получен не корректный формат данных")
    return file


async def save_file(file_, photo=False):
    new_name = f'{uuid4()}.{file_.filename.rsplit(".")[-1]}'
    path_file = os.path.join(config.MUSICS_FOLDER if not photo else config.PHOTOS_FOLDER, new_name)

    try:
        async with aiofiles.open(path_file, 'wb') as f:
            while contents := file_.file.read(1024 * 1024):
                await f.write(contents)
    except Exception as e:
        print(e)
        raise HTTPException(500, detail="Произошла ошибка в обработке файла")
    finally:
        file_.file.close()

    try:
        content_type = file_.content_type
    except Exception as e:
        print(e)
        content_type = None

    return new_name, path_file, content_type


def get_data_music_default(file_name):
    split_file_name = file_name.split('-')
    if len(split_file_name) == 1:
        author_, name_ = 'Неизвестен', split_file_name[0].split('.')[0].strip()
    else:
        name_ = split_file_name[1].split('.')[0].strip()
        author_ = split_file_name[0].strip()
    return name_, author_


def calculating_human_duration(length):
    hours = length // 3600  # calculate in hours
    length %= 3600
    mins = length // 60  # calculate in minutes
    length %= 60
    seconds = length  # calculate in seconds
    if hours == 0:
        return f'{mins // 10}{mins % 10}:{seconds // 10}{seconds % 10}'
    return f'{hours//10}{hours%10}:{mins//10}{mins%10}:{seconds//10}{seconds%10}'


def get_data_music_with_tinytag(path_file_):
    name, author, duration, genre, picture = None, None, None, None, None
    try:
        tag = TinyTag.get(path_file_, image=True)
        name, author, duration, genre, picture = tag.title, tag.artist, tag.duration, tag.genre, tag.get_image()
    except Exception as e:
        print(e)
    if duration is None:
        with audioread.audio_open(path_file_) as f:
            duration = calculating_human_duration(int(f.duration))
    else:
        duration = calculating_human_duration(int(duration))
    return name, author, duration, genre, picture


async def processed_audio(file_, user_id_):
    new_name_, path_file_, content_type_ = await save_file(file_, photo=False)

    name, author, duration, genre, picture = get_data_music_with_tinytag(path_file_)

    if name is None or author is None:
        name, author = get_data_music_default(file_.filename)

    name = escape(name)
    author = escape(author)

    if len(name) > 200 or len(author) > 200:
        raise HTTPException(406, detail="Название песни не должно превышать 90 символов")

    get_image = 1  # идентификатор дефолтной картинки
    if picture is not None:
        new_cover_name = f'{uuid4()}.jpg'
        with open(os.path.join(config.PHOTOS_FOLDER, new_cover_name), 'wb') as f:
            f.write(picture)

        await query_execute(
            query_text=f'insert into "Images" (content_type, file_name) values (\'image/jpeg\', \'{new_cover_name}\')',
            fetch_all=False,
            type_query='insert'
        )

        get_image = await query_execute(
            query_text=f'select * from "Images" as I where I.file_name = \'{new_cover_name}\'',
            fetch_all=False,
            type_query='read'
        )
        get_image = get_image.id

    await query_execute(
        query_text=f'insert into "Musics" (name, author, genre, cover, filename, duration, datetime_add, user_id_add) '
                   f'values (\'{name}\', \'{author}\', \'{genre}\', {get_image}, '
                   f'\'{new_name_}\', \'{duration}\', \'{datetime.now()}\', {user_id_})',
        fetch_all=False,
        type_query='insert'
    )

    get_music = await query_execute(
        query_text=f'select * from "Musics" as M where M.user_id_add = {user_id_} and M.filename = \'{new_name_}\''
    )

    if get_music is None:
        raise HTTPException(500, detail="Внутренняя ошибка сервера")

    async with Session() as db:
        await db.execute(text('BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE'))
        await db.execute(text(
            f'insert into "Collections" (track_number, datetime_add, music_id, playlist_id) '
            f'values ('
            f'(select coalesce(max(C.track_number), 0) from "Collections" as C where C.playlist_id = 1) + 1, '
            f'\'{datetime.now()}\', '
            f'{get_music.id}, '
            f'(select PL.id from "PlayLists" as PL '
            f'where PL.user_id = {user_id_} and PL.name = \'Вся моя музыка\'));'
        ))
        await db.execute(text('commit'))

    result = FileResponse(
        result=True,
        message='Лютый музон загружен',
        data=File(
            type='music',
            file_data=Music(
                id=get_music.id,
                number=None,
                name=get_music.name,
                author=get_music.author,
                genre=get_music.genre,
                cover=f'{config.API_IMAGE}{get_music.cover}',
                path=f'{config.API_MUSIC}{get_music.id}',
                duration=get_music.duration,
                datetime_add=get_music.datetime_add,
                can_edit=True
            )
        )
    )
    return result.json()


async def processed_photo(file_, action_, music_id_, user_id_):
    if action_ == 'cover':

        if music_id_ is None:
            raise HTTPException(406, detail="Идентификатор трека не указан")

        get_music = await query_execute(
            query_text=f'select * from "Musics" as M where M.id = {music_id_}',
            fetch_all=False,
            type_query='read'
        )
        if get_music is None:
            raise HTTPException(404, detail="Трек не найден")

        if get_music.user_id_add != user_id_:
            raise HTTPException(403, detail="У вас нет прав на редактирования этого трека")

    new_name_, path_file_, content_type_ = await save_file(file_, photo=True)

    await query_execute(
        query_text=f'insert into "Images" (content_type, file_name) values (\'{content_type_}\', \'{new_name_}\')',
        fetch_all=False,
        type_query='insert'
    )

    get_image = await query_execute(
        query_text=f'select * from "Images" as I where I.file_name = \'{new_name_}\'',
        fetch_all=False,
        type_query='read'
    )

    if action_ == 'avatar':
        await query_execute(
            query_text=f'update "Users" as U set (avatar) = ({get_image.id}) where U.id = {user_id_}',
            fetch_all=False,
            type_query='update'
        )
    if action_ == 'cover':
        await query_execute(
            query_text=f'update "Musics" as M set (cover) = ({get_image.id}) where M.id = {music_id_}',
            fetch_all=False,
            type_query='update'
        )

    result = FileResponse(
        result=True,
        message='Лютый музон загружен',
        data=File(
            type='music',
            file_data=Photo(
                path=f'{config.MAIN_URL}/api/image/{get_image.id}'
            )
        )
    )
    return result.json()


async def load_and_save_file(file_, action_, user_id_, music_id_=None):
    file = await validate_file(file_, action_)
    if action_ == 'music':
        yield await processed_audio(file, user_id_)
    else:
        yield await processed_photo(file, action_, music_id_, user_id_)
