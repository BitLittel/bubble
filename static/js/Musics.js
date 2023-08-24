function getAllUserMusics(playlist_id) {
    sendRequest(
        'GET',
        '/api/playlist/'+playlist_id,
        true,
        null,
        function (data) {
            console.log(data);
            InitMusic(data.data);
        },
        function (data) {
            console.log(data);
        }
    );
}

function UploadTrack() {
    let add_track = document.getElementById('add_track');

    add_track.style.display = 'flex';
}