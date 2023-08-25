let main_input_music_upload = document.getElementById('music_file'),
    button_select_upload_music = document.getElementById('button_select_upload_music'),
    list_uploaded_music = document.getElementById('list_uploaded_music'),
    count_all_file = 0,
    limit_uploading_file = 5,
    count_finished_file = 0,
    queue_file = [];

function showUpload() {
    document.getElementById('upload').style.display = 'block';
    document.getElementsByTagName('body')[0].style.overflow = 'hidden';
}

function closeUpload(target) {
    if (event.target == target) {
        document.getElementById('upload').style.display = 'none';
        document.getElementsByTagName('body')[0].style.overflow = 'auto';
    }
}

main_input_music_upload.addEventListener('change', UploadFile);

function PrepareUpload() {
    main_input_music_upload.click();
}

function ProcessingFile(index_, file_) {
    let request = new XMLHttpRequest(),
        formData = new FormData;

    request.open('POST', '/api/upload_file', true);

    formData.append('action', 'music');
    formData.append('file', file_);

    request.upload.onloadstart = function () {
        document.getElementById('status_loading_track_'+index_).innerText = '0%';
    };

    request.upload.onprogress = function (event) {
        let percents = ((event.loaded/event.total)*100).toFixed(2);
        document.getElementById('status_loading_track_'+index_).innerText = percents+'%';
    };

    request.upload.onloadend = function () {
        document.getElementById('status_yes_track_'+index_).style.display = 'block';
        document.getElementById('status_loading_track_'+index_).style.display = 'none';
    };

    request.onload = function () {
        let responseObj = JSON.parse(request.response);
        console.log(responseObj);

        if (request.status == 400 || request.status == 409) {
            show_error(responseObj.detail, 'Ошибка');
        }

        if (responseObj.result == true) {
            document.getElementById('cover_track_'+index_).src = responseObj.data.file_data.cover;
            document.getElementById('name_track_'+index_).innerText = responseObj.data.file_data.author+" - "+responseObj.data.file_data.name

            count_finished_file += 1;
            console.log('ИКРЕМЕНТИРУЕМ ФИНИШ!', count_finished_file);

            if (queue_file.length !== 0) {
                console.log('ОЧЕРЕДЬ НЕ ПУСТА', queue_file.length);
                let task = queue_file.shift();
                console.log(task);
                ProcessingFile(task[0], task[1]);
            } else {
                console.log('ОЧЕРЕДЬ ПУСТА!!!!!!!!!', count_finished_file);
                if (count_all_file === count_finished_file) {
                    console.log('REDIRECT!!!!!!!!');
                    window.location = '/';
                }
            }
        } else {
            show_error(responseObj.detail, 'Ошибка');
        }
    };
    request.send(formData);
}

function generateDomUploadedTrack(index, name_track) {
    let div_uploaded_track = document.createElement('div'),
        img_cover_track = document.createElement('img'),
        span_name_track = document.createElement('span'),
        div_status = document.createElement('div'),
        img_status_yes = document.createElement('img'),
        span_status_loading = document.createElement('span');

    div_uploaded_track.className = 'uploaded_track';
    div_uploaded_track.id = 'track_'+index;
    div_uploaded_track.appendChild(img_cover_track);

    img_cover_track.className = 'default_img';
    img_cover_track.id = 'cover_track_'+index;
    img_cover_track.src = 'http://192.168.0.100:8000/api/image/1';

    div_uploaded_track.appendChild(span_name_track);
    span_name_track.id = 'name_track_'+index;
    span_name_track.innerText = name_track;

    div_uploaded_track.appendChild(div_status);

    div_status.appendChild(img_status_yes);
    img_status_yes.id = 'status_yes_track_'+index;
    img_status_yes.className = 'default_img';
    img_status_yes.style.display = 'none';
    img_status_yes.style.border = 'none';
    img_status_yes.src = '../static/img/yes.png';

    div_status.appendChild(span_status_loading);
    span_status_loading.id = 'status_loading_track_'+index;
    span_status_loading.style.display = 'block';
    span_status_loading.innerText = '0%';
    return div_uploaded_track
}

function UploadFile(e) {
    let target = e.target,
        files = target.files;

    button_select_upload_music.style.display = 'none';
    count_all_file = files.length;

    for (let i = 0; i < files.length; i++) {
        queue_file.push([i, files[i]]);

        list_uploaded_music.appendChild(
            generateDomUploadedTrack(i, files[i].name)
        );
    }

    for (let j = 0; j < limit_uploading_file; j++) {
        if (queue_file.length != 0) {
            let task = queue_file.shift();
            console.log(task);
            ProcessingFile(task[0], task[1]);
        } else {
            break;
        }
    }
}