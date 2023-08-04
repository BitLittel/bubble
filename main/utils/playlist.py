from main.models.database import query_execute
from main.schemas.playlist import ResponseAllPlayList, PlayList, PlayListWithMusic, PlayListAndMusic
from main.schemas.music import Music


async def get_all_playlists_user_with_user_id(user_id: id) -> ResponseAllPlayList | bool:
    get_user_all_playlist = await query_execute(
        query_text=f'select * from "PlayLists" as PL where PL.user_id = {user_id} order by PL.datetime_add',
        fetch_all=True,
        type_query='read'
    )
    if get_user_all_playlist is not None:
        return ResponseAllPlayList(
            result=True,
            message="Успех",
            data=[
                PlayList(
                    playlist_id=i.id,
                    playlist_name=i.name,
                    playlist_cover=i.cover,
                    playlist_datetime_add=i.datetime_add,
                    can_edit=True
                ) for i in get_user_all_playlist
            ]
        )
    else:
        return False


async def get_playlist_by_id(id_playlist: int, user_id: int) -> PlayListWithMusic | bool:
    playlist = await query_execute(
        query_text=f'select * from "PlayLists" as PL where PL.id = {id_playlist}',
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
                       f'M.picture as track_cover, '
                       f'M.path as track_path, '
                       f'M.time_duration as track_duration, '
                       f'M.datetime_add as track_datetime_add, '
                       f'M.user_id_add '
                       f'from "Collections" as C '
                       f'left join "Musics" M on C.music_id = M.id '
                       f'where C.playlist_id = {id_playlist}',
            fetch_all=True,
            type_query='read'
        )

        return PlayListWithMusic(
            result=True,
            message="Успех",
            data=PlayListAndMusic(
                playlist=PlayList(
                    playlist_id=playlist.id,
                    playlist_name=playlist.name,
                    playlist_cover=playlist.cover,
                    playlist_datetime_add=playlist.datetime_add,
                    can_edit=playlist.user_id == user_id
                ),
                musics=[
                    Music(
                        track_id=i.track_id,
                        track_number=i.track_number,
                        track_name=i.track_name,
                        track_author=i.track_author,
                        track_genre=i.track_genre,
                        track_cover=i.track_cover,
                        track_path=i.track_path,
                        track_duration=i.track_duration,
                        track_datetime_add=i.track_datetime_add,
                        user_id_add=i.user_id_add
                    ) for i in musics_from_playlist
                ]
            )
        )

    return False
