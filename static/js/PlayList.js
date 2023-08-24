let main_playlist = document.getElementById('playlists'),
    button_add_playlist = document.getElementById('button_add_playlist');

function generatePlayLists(playlists) {
    main_playlist.style.display = 'flex';

    for (let i = 0; i < playlists.length; i++) {
        let div_blockPlayList = document.createElement('div'),
            img_cover = document.createElement('img'),
            span_name = document.createElement('span');
        div_blockPlayList.className = 'blockPlayList';
        div_blockPlayList.appendChild(img_cover);
        img_cover.src = playlists[i].cover;
        div_blockPlayList.appendChild(span_name);
        span_name.innerText = playlists[i].name;

        if (playlists[i].name === 'Вся моя музыка') {getAllUserMusics(playlists[i].id);}

        button_add_playlist.before(div_blockPlayList);
    }
}

function getPlayLists() {
    sendRequest(
        'GET',
        '/api/playlist',
        true,
        null,
        function (data) {
            console.log(data);
            generatePlayLists(data.data);
        },
        function (data) {
            console.log(data);
        }
    );
}