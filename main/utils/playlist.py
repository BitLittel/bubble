import datetime
from main.models.database import query_execute
from main.schemas.playlist import ResponseAllPlayList, PlayList, PlayListWithMusic, PlayListAndMusic
from main.schemas.music import Music
from main import config


async def get_un_auth_playlist() -> PlayListWithMusic:
    get_random_music = await query_execute(
        query_text=f'select '
                   f'M.id as track_id, '
                   f'M.name as track_name, '
                   f'M.author as track_author, '
                   f'M.genre as track_genre, '
                   f'CONCAT(\'{config.API_IMAGE}\', M.cover) as track_cover, '
                   f'CONCAT(\'{config.API_MUSIC}\', M.id) as track_path, '
                   f'M.duration as track_duration, '
                   f'M.datetime_add as track_datetime_add '
                   f' from "Musics" as M order by random() limit 20',
        fetch_all=True,
        type_query='read'
    )
    if get_random_music == []:
        return PlayListWithMusic(
            result=True,
            message="Успех",
            data=PlayListAndMusic(
                track_count=20,
                current_track={},
                playlist=PlayList(
                    id=0,
                    name='UnAuthPlayList',
                    cover='/static/img/default_img.jpg',
                    datetime_add=datetime.datetime.now(),
                    can_edit=False
                ),
                track_list={}
            )
        )
    return PlayListWithMusic(
        result=True,
        message="Успех",
        data=PlayListAndMusic(
            track_count=20,
            current_track={
                0: Music(
                    id=get_random_music[0].track_id,
                    name=get_random_music[0].track_name,
                    author=get_random_music[0].track_author,
                    genre=get_random_music[0].track_genre,
                    cover=get_random_music[0].track_cover,
                    path=get_random_music[0].track_path,
                    duration=get_random_music[0].track_duration,
                    datetime_add=get_random_music[0].track_datetime_add,
                    can_edit=False
                )
            },
            playlist=PlayList(
                id=0,
                name='UnAuthPlayList',
                cover='/static/img/default_img.jpg',
                datetime_add=datetime.datetime.now(),
                can_edit=False
            ),
            track_list={
                i: Music(
                    id=get_random_music[i].track_id,
                    name=get_random_music[i].track_name,
                    author=get_random_music[i].track_author,
                    genre=get_random_music[i].track_genre,
                    cover=get_random_music[i].track_cover,
                    path=get_random_music[i].track_path,
                    duration=get_random_music[i].track_duration,
                    datetime_add=get_random_music[i].track_datetime_add,
                    can_edit=False
                ) for i in range(len(get_random_music))
            }
        )
    )


async def get_playlists_with_user_id(user_id: id) -> ResponseAllPlayList | bool:
    # todo: переписать на то что у пользователя теперь liked_playlist
    get_user_all_playlist = await query_execute(
        query_text=f'select '
                   f'PL.id,'
                   f'PL.name,'
                   f'CONCAT(\'{config.API_IMAGE}\', PL.cover) as cover, '
                   f'PL.datetime_add '
                   f'from "PlayLists" as PL '
                   f'where PL.user_id = {user_id} '
                   f'order by PL.datetime_add',
        fetch_all=True,
        type_query='read'
    )
    if get_user_all_playlist is not None:
        return ResponseAllPlayList(
            result=True,
            message="Успех",
            data=[
                PlayList(
                    id=i.id,
                    name=i.name,
                    cover=i.cover,
                    datetime_add=i.datetime_add,
                    can_edit=True
                ) for i in get_user_all_playlist
            ]
        )
    else:
        return False


async def get_playlist_by_id(id_playlist: int, user_id: int) -> PlayListWithMusic | bool:
    playlist = await query_execute(
        query_text=f'select '
                   f'PL.id, '
                   f'PL.name, '
                   f'CONCAT(\'{config.API_IMAGE}\', PL.cover) as cover, '
                   f'PL.datetime_add, '
                   f'PL.user_id,'
                   f'(select count(*) from "Collections" as CC where CC.playlist_id = PL.id) as track_count '
                   f'from "PlayLists" as PL '
                   f'where PL.id = {id_playlist}',
        fetch_all=False,
        type_query='read'
    )

    if playlist is None:
        return False

    musics_from_playlist = await query_execute(
        query_text=f'select M.id as track_id, '
                   f'M.name as track_name, '
                   f'M.author as track_author, '
                   f'M.genre as track_genre, '
                   f'CONCAT(\'{config.API_IMAGE}\', M.cover) as track_cover, '
                   f'CONCAT(\'{config.API_MUSIC}\', M.id) as track_path, '
                   f'M.duration as track_duration, '
                   f'M.datetime_add as track_datetime_add, '
                   f'M.user_id_add '
                   f'from "Collections" as C '
                   f'left join "Musics" M on C.music_id = M.id '
                   f'where C.playlist_id = {id_playlist} '
                   f'order by M.datetime_add desc',
        fetch_all=True,
        type_query='read'
    )
    if musics_from_playlist == []:
        return PlayListWithMusic(
            result=True,
            message="Успех",
            data=PlayListAndMusic(
                track_count=0,
                current_track={},
                playlist=PlayList(
                    id=playlist.id,
                    name=playlist.name,
                    cover=playlist.cover,
                    datetime_add=playlist.datetime_add,
                    can_edit=playlist.user_id == user_id
                ),
                track_list={}
            )
        )
    return PlayListWithMusic(
        result=True,
        message="Успех",
        data=PlayListAndMusic(
            track_count=playlist.track_count,
            # todo: задел на будущее, в current_track можно передавать
            #  трек на котором остановился и типо на всех устройствах типо синхрониться
            current_track={
                0: Music(
                    id=musics_from_playlist[0].track_id,
                    name=musics_from_playlist[0].track_name,
                    author=musics_from_playlist[0].track_author,
                    genre=musics_from_playlist[0].track_genre,
                    cover=musics_from_playlist[0].track_cover,
                    path=musics_from_playlist[0].track_path,
                    duration=musics_from_playlist[0].track_duration,
                    datetime_add=musics_from_playlist[0].track_datetime_add,
                    can_edit=musics_from_playlist[0].user_id_add == user_id
                )
            },
            playlist=PlayList(
                id=playlist.id,
                name=playlist.name,
                cover=playlist.cover,
                datetime_add=playlist.datetime_add,
                can_edit=playlist.user_id == user_id
            ),
            track_list={
                i: Music(
                    id=musics_from_playlist[i].track_id,
                    name=musics_from_playlist[i].track_name,
                    author=musics_from_playlist[i].track_author,
                    genre=musics_from_playlist[i].track_genre,
                    cover=musics_from_playlist[i].track_cover,
                    path=musics_from_playlist[i].track_path,
                    duration=musics_from_playlist[i].track_duration,
                    datetime_add=musics_from_playlist[i].track_datetime_add,
                    can_edit=musics_from_playlist[i].user_id_add == user_id
                ) for i in range(len(musics_from_playlist))
            }
        )
    )

