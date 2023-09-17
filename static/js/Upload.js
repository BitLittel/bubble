let main_input_music_upload = document.getElementById('music_file'),
    button_select_upload_music = document.getElementById('button_select_upload_music'),
    list_uploaded_music = document.getElementById('list_uploaded_music'),
    count_all_file = 0,
    count_finished_file = 0,
    queue_file = [];

main_input_music_upload.addEventListener('change', UploadFile);

function PrepareUpload() {
    main_input_music_upload.click();
}

function UploadFile(e) {
    let target = e.target,
        files = target.files;

    if (files.length !== 0) {
        button_select_upload_music.style.display = 'none';
        count_all_file = files.length;
        list_uploaded_music.style.display = 'block';

        for (let i = 0; i < files.length; i++) {
            queue_file.push([i, files[i]]);

            list_uploaded_music.appendChild(
                generateDomUploadedTrack(i, files[i].name)
            );
        }

        if (queue_file.length !== 0) {
            let task = queue_file.shift();
            ProcessingFile(task[0], task[1]);
        }
    }
}

function ProcessingFile(index_, file_) {
    let request = new XMLHttpRequest(),
        formData = new FormData;

    request.open('POST', '/api/upload_file', true);

    formData.append('action', 'music');
    formData.append('file', file_);

    request.upload.onloadstart = function () {
        document.getElementById('uploaded_status_'+index_).innerText = 'Загрузка... 0%';
    };

    request.upload.onprogress = function (event) {
        let percents = ((event.loaded/event.total)*100).toFixed(2);
        document.getElementById('uploaded_progress_bar_'+index_).style.width = percents+'%';
        document.getElementById('uploaded_status_'+index_).innerText = 'Загрузка... '+ percents +'%';
    };

    request.upload.onloadend = function () {
        document.getElementById('uploaded_status_'+index_).innerText = 'Загрузка завершена';
    };

    request.onload = function () {
        let responseObj = JSON.parse(request.response);
        console.log(responseObj);

        if (request.status == 400 || request.status == 409) {
            document.getElementById('uploaded_status_'+index_).innerText = 'Ошибка: '+responseObj.detail;
            //show_error(false, responseObj.detail, 'Ошибка');
        }
        if (responseObj.result == true) {
            document.getElementById('upload_cover_'+index_).src = responseObj.data.file_data.cover;
            document.getElementById('uploaded_name_'+index_).innerText = responseObj.data.file_data.author+" - "+responseObj.data.file_data.name;
            count_finished_file += 1;
        } else {
            document.getElementById('uploaded_status_'+index_).innerText = 'Ошибка: '+responseObj.detail;
            //show_error(false, responseObj.detail, 'Ошибка');
            count_finished_file += 1;
        }
        if (queue_file.length !== 0) {
            let task = queue_file.shift();
            ProcessingFile(task[0], task[1]);
        } else {
            if (count_all_file === count_finished_file) {
                console.log('REDIRECT!!!!!!!!');
                window.location = '/';
            }
        }
    };
    request.send(formData);
}

function generateDomUploadedTrack(index, name_track) {
    let div_upload_music = document.createElement('div'),
        img_upload_cover = document.createElement('img'),
        div_title_playlist = document.createElement('div'),
        p_uploaded_name = document.createElement('p'),
        p_uploaded_status = document.createElement('p'),
        div_main_player_full_time_line = document.createElement('div'),
        div_uploaded_progress_bar = document.createElement('div');

    div_upload_music.id = 'upload_music_'+index;
    div_upload_music.className = 'block_upload_music';
    div_upload_music.appendChild(img_upload_cover);
        img_upload_cover.className = 'music_cover';
        img_upload_cover.src = '/static/img/default_img.jpg';
        img_upload_cover.id = 'upload_cover_'+index;
    div_upload_music.appendChild(div_title_playlist);
        div_title_playlist.className = 'title_playlist';
        div_title_playlist.style.width = '100%';
        div_title_playlist.appendChild(p_uploaded_name);
            p_uploaded_name.id = 'uploaded_name_'+index;
            p_uploaded_name.innerText = name_track;
        div_title_playlist.appendChild(p_uploaded_status);
            p_uploaded_status.id = 'uploaded_status_'+index;
            p_uploaded_status.innerText = 'Ожидание...';
        div_title_playlist.appendChild(div_main_player_full_time_line);
            div_main_player_full_time_line.className = 'main_player_full_time_line';
            div_main_player_full_time_line.appendChild(div_uploaded_progress_bar);
                div_uploaded_progress_bar.className = 'main_player_cur_time_line';
                div_uploaded_progress_bar.id = 'uploaded_progress_bar_'+index;
                div_uploaded_progress_bar.style.width = '0%';
    return div_upload_music
}
