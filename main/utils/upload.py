import os
import hashlib
import aiofiles
import audioread
from uuid import uuid4
from main import config
from tinytag import TinyTag
from sqlalchemy import text
from datetime import datetime
from fastapi import HTTPException
from main.schemas.music import Music
from main.models.database import Session
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
        raise HTTPException(500, detail="Произошла ошибка в обработке файла")
    finally:
        file_.file.close()

    try:
        content_type = file_.content_type
    except Exception as e:
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
    return f'{hours // 10}{hours % 10}:{mins // 10}{mins % 10}:{seconds // 10}{seconds % 10}'


async def get_data_music_with_tinytag(path_file_):
    name, author, duration, genre, picture = None, None, None, None, None
    try:
        tag = TinyTag.get(path_file_, image=True)
        name, author, duration, genre, picture = tag.title, tag.artist, tag.duration, tag.genre, tag.get_image()
    except Exception as e:
        pass
    if duration is None:
        with audioread.audio_open(path_file_) as f:
            duration = calculating_human_duration(int(f.duration))
    else:
        duration = calculating_human_duration(int(duration))
    return name, author, duration, genre, picture


async def compute_sha256(path_file_):
    hash_sha256 = hashlib.sha256()
    with open(path_file_, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def audio_response(audio_object):
    result = FileResponse(
        result=True,
        message='Лютый музон загружен',
        data=File(
            type='music',
            file_data=Music(
                id=audio_object.id,
                number=None,
                name=audio_object.name,
                author=audio_object.author,
                genre=audio_object.genre,
                cover=f'{config.API_IMAGE}{audio_object.cover}',
                path=f'{config.API_MUSIC}{audio_object.id}',
                duration=audio_object.duration,
                datetime_add=audio_object.datetime_add,
                can_edit=True
            )
        )
    )
    return result.json()


async def processed_audio(file_, user_id_):
    new_name_, path_file_, content_type_ = await save_file(file_, photo=False)

    # check == audio
    hash_of_file = await compute_sha256(path_file_)
    find_collision = await query_execute(
        query_text=f'select * from "Musics" as M where M.hashsum = \'{hash_of_file}\'',
        fetch_all=False,
        type_query='read'
    )
    if find_collision is not None:
        find_track_in_collection = await query_execute(
            query_text=f'select PL.id as playlist_id, C.id as collection_id '
                       f'from "PlayLists" as PL '
                       f'left join "Collections" as C on C.playlist_id = PL.id and C.music_id = {find_collision.id} '
                       f'where PL.user_id = {user_id_} and PL.name = \'Вся моя музыка\'',
            fetch_all=False,
            type_query='read'
        )
        if find_track_in_collection.collection_id is None:
            await query_execute(
                query_text=f'insert into "Collections" (datetime_add, music_id, playlist_id) '
                           f'values '
                           f'(\'{datetime.now()}\', {find_collision.id}, {find_track_in_collection.playlist_id});',
                fetch_all=False,
                type_query='insert'
            )
        os.remove(path_file_)
        return audio_response(find_collision)

    name, author, duration, genre, picture = await get_data_music_with_tinytag(path_file_)

    if name is None or author is None:
        name, author = get_data_music_default(file_.filename)

    name = "Без название" if name is None else name
    author = "Неизвестен" if author is None else author

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

    async with Session() as db:
        await db.execute(
            text(
                f'insert into "Musics" (name, author, genre, cover, filename, duration, '
                f'datetime_add, user_id_add, hashsum) '
                f'values (:name_, :author, :genre, :get_image, :new_name_, :duration, :datetime, :user_id_, :hash_sum)'
            ),
            {
                'name_': name, 'author': author, 'genre': genre, 'get_image': get_image, 'new_name_': new_name_,
                'duration': duration, 'datetime': datetime.now(), 'user_id_': user_id_, 'hash_sum': hash_of_file
            }
        )
        await db.execute(text('COMMIT'))

    get_music = await query_execute(
        query_text=f'select * from "Musics" as M where M.user_id_add = {user_id_} and M.filename = \'{new_name_}\'',
        type_query='read',
        fetch_all=False
    )

    get_default_playlist = await query_execute(
        query_text=f'select PL.id from "PlayLists" as PL where PL.user_id={user_id_} and PL.name=\'Вся моя музыка\'',
        fetch_all=False,
        type_query='read'
    )

    if get_music is None:
        raise HTTPException(500, detail="Внутренняя ошибка сервера")

    await query_execute(
        query_text=f'insert into "Collections" (datetime_add, music_id, playlist_id) '
                   f'values '
                   f'(\'{datetime.now()}\', {get_music.id}, {get_default_playlist.id});',
        fetch_all=False,
        type_query='insert'
    )

    return audio_response(get_music)


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
