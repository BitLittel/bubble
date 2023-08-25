from main.models.database import query_execute
from main.schemas.playlist import ResponseAllPlayList, PlayList, PlayListWithMusic, PlayListAndMusic
from main.schemas.music import Music
from main import config


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
                   f'PL.user_id '
                   f'from "PlayLists" as PL '
                   f'where PL.id = {id_playlist}',
        fetch_all=False,
        type_query='read'
    )
    if playlist is not None:
        musics_from_playlist = await query_execute(
            query_text=f'select M.id as track_id, '
                       f'C.track_number as track_number, '
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

        get_max_track_number = await query_execute(
            query_text=f'select max(CC.track_number) as max_track_number '
                       f'from "Collections" as CC where CC.playlist_id = {id_playlist}',
            fetch_all=False,
            type_query='read'
        )
        if get_max_track_number is None or get_max_track_number.max_track_number is None:
            get_max_track_number = 1
        else:
            get_max_track_number = get_max_track_number.max_track_number

        return PlayListWithMusic(
            result=True,
            message="Успех",
            data=PlayListAndMusic(
                # todo: задел на будущее, в current_track_number можно передавать
                #  трек на котором остановился и типо на всех устройствах типо синхрониться
                current_track_number=1,
                last_track_number=get_max_track_number,
                playlist=PlayList(
                    id=playlist.id,
                    name=playlist.name,
                    cover=playlist.cover,
                    datetime_add=playlist.datetime_add,
                    can_edit=playlist.user_id == user_id
                ),
                track_list=[
                    Music(
                        id=i.track_id,
                        number=i.track_number,
                        name=i.track_name,
                        author=i.track_author,
                        genre=i.track_genre,
                        cover=i.track_cover,
                        path=i.track_path,
                        duration=i.track_duration,
                        datetime_add=i.track_datetime_add,
                        can_edit=i.user_id_add == user_id
                    ) for i in musics_from_playlist
                ]
            )
        )
    return False
